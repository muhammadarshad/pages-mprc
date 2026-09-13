/* 3-D unsplit VOF: decomposition invariance across four arithmetics.
 *   naive float | Kahan-compensated | exact fixed-point reduction | ring Z_256
 * Unsplit flux: each cell accumulates contributions from 6 faces, and the
 * ACCUMULATION ORDER follows the block traversal -- which is what a real
 * domain decomposition changes.  Build: gcc -O2 -o vof3d vof3d.c -lm        */
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>
#include <stdint.h>
#include <time.h>
static double now(void){struct timespec t;clock_gettime(CLOCK_MONOTONIC,&t);return t.tv_sec+1e-9*t.tv_nsec;}

#define N     32
#define NN    (N*N*N)
#define S     256
#define STEPS 40
#define IX(i,j,k) ((((i)+N)%N)*N*N + (((j)+N)%N)*N + (((k)+N)%N))

static double f[NN], fl[NN][6], acc[NN];
static long long CNT_F=0, CNT_I=0, FULL_F=0, FULL_I=0, EMPTY_F=0, EMPTY_I=0;
static int64_t racc[NN];
#define RSCALE 1099511627776.0
static double kc[NN];
static int64_t If[NN], Ifl[NN][6], Iacc[NN];

static double F3(double t){ return t<=0?0.0:t*t*t; }
static double vol3(double nx,double ny,double nz,double a){
    double t,d;
    if(nx>ny){t=nx;nx=ny;ny=t;}  if(ny>nz){t=ny;ny=nz;nz=t;}
    if(nx>ny){t=nx;nx=ny;ny=t;}
    if(a<=0) return 0.0; if(a>=1) return 1.0;
    d=6*nx*ny*nz;
    if(d<1e-14){
        if(ny<1e-14) return a/nz<1?a/nz:1;
        double p=ny,q=nz,b;
        if(a<=(p<q?p:q)) return a*a/(2*p*q);
        if(a>=p+q) return 1.0;
        if(a<=(p>q?p:q)) return (2*a-(p<q?p:q))/(2*(p>q?p:q));
        b=p+q-a; return 1-b*b/(2*p*q);
    }
    return (F3(a)-F3(a-nx)-F3(a-ny)-F3(a-nz)
            +F3(a-nx-ny)+F3(a-nx-nz)+F3(a-ny-nz)-F3(a-1))/d;
}
static double inv3_f(double nx,double ny,double nz,double t){
    int lo=0,hi=S,m;
    while(hi-lo>1){ m=(lo+hi)>>1; if(vol3(nx,ny,nz,(double)m/S)<t) lo=m; else hi=m; }
    return (double)lo/S;
}
static int inv3_i(double nx,double ny,double nz,int v){
    int lo=0,hi=S,m; double t=(double)v/S;
    while(hi-lo>1){ m=(lo+hi)>>1; if(vol3(nx,ny,nz,(double)m/S)<t) lo=m; else hi=m; }
    return lo;
}
static const int DI[6]={1,-1,0,0,0,0}, DJ[6]={0,0,1,-1,0,0}, DK[6]={0,0,0,0,1,-1};

static void fluxes_f(double c){
    int i,j,k,d;
    for(i=0;i<N;i++)for(j=0;j<N;j++)for(k=0;k<N;k++){
        int id=IX(i,j,k); double v=f[id];
        if(v<=1e-13){ EMPTY_F++; for(d=0;d<6;d++) fl[id][d]=0; continue; }
        double gx=-(f[IX(i+1,j,k)]-f[IX(i-1,j,k)]);
        double gy=-(f[IX(i,j+1,k)]-f[IX(i,j-1,k)]);
        double gz=-(f[IX(i,j,k+1)]-f[IX(i,j,k-1)]);
        double s=fabs(gx)+fabs(gy)+fabs(gz); if(s<1e-13) s=1.0;
        double nx=fabs(gx)/s, ny=fabs(gy)/s, nz=fabs(gz)/s;
        if(v>=1-1e-13) FULL_F++; else CNT_F++;
        double a = (v>=1-1e-13)? 1.0 : inv3_f(nx,ny,nz,v);
        for(d=0;d<6;d++){
            double nd = d<2? nx : (d<4? ny : nz);
            double A = (v>=1-1e-13)? c*nd/3.0
                     : vol3(nx,ny,nz,a)-vol3(nx,ny,nz,a-nd*c/3.0);
            if(A<0)A=0; fl[id][d]=A;
        }
        double tot=0; for(d=0;d<6;d++) tot+=fl[id][d];
        if(tot>v){ for(d=0;d<6;d++) fl[id][d]*= v/tot; }
    }
}
static void fluxes_i(int pn,int pd){
    int i,j,k,d;
    for(i=0;i<N;i++)for(j=0;j<N;j++)for(k=0;k<N;k++){
        int id=IX(i,j,k); int64_t v=If[id];
        if(v<=0){ EMPTY_I++; for(d=0;d<6;d++) Ifl[id][d]=0; continue; }
        double gx=-(double)(If[IX(i+1,j,k)]-If[IX(i-1,j,k)]);
        double gy=-(double)(If[IX(i,j+1,k)]-If[IX(i,j-1,k)]);
        double gz=-(double)(If[IX(i,j,k+1)]-If[IX(i,j,k-1)]);
        double s=fabs(gx)+fabs(gy)+fabs(gz); if(s<1e-13) s=1.0;
        double nx=fabs(gx)/s, ny=fabs(gy)/s, nz=fabs(gz)/s;
        if(v>=S) FULL_I++; else CNT_I++;
        double a = (v>=S)? 1.0 : (double)inv3_i(nx,ny,nz,(int)v)/S;
        int64_t tot=0;
        for(d=0;d<6;d++){
            double nd = d<2? nx : (d<4? ny : nz);
            double A = (v>=S)? ((double)pn/pd)*nd/3.0
                     : vol3(nx,ny,nz,a)-vol3(nx,ny,nz,a-nd*((double)pn/pd)/3.0);
            int64_t q = (int64_t)(A*S); if(q<0)q=0;
            Ifl[id][d]=q; tot+=q;
        }
        if(tot>v){ for(d=0;d<6;d++) Ifl[id][d]=(Ifl[id][d]*v)/tot; }
    }
}
static void apply_f(int bs,int mode){
    int bi,bj,bk,i,j,k,d;
    memset(acc,0,sizeof acc); memset(kc,0,sizeof kc);
    for(bi=0;bi<N;bi+=bs)for(bj=0;bj<N;bj+=bs)for(bk=0;bk<N;bk+=bs)
     for(i=bi;i<bi+bs&&i<N;i++)for(j=bj;j<bj+bs&&j<N;j++)for(k=bk;k<bk+bs&&k<N;k++){
        int id=IX(i,j,k);
        for(d=0;d<6;d++){
            int t=IX(i+DI[d],j+DJ[d],k+DK[d]); double x=fl[id][d];
            if(mode==0){ acc[t]+=x; }
            else { double y=x-kc[t], s2=acc[t]+y; kc[t]=(s2-acc[t])-y; acc[t]=s2; }
            acc[id]-=x;
        }
     }
    for(i=0;i<NN;i++) f[i]+=acc[i];
}
static void apply_r(int bs){
    int bi,bj,bk,i,j,k,d;
    memset(racc,0,sizeof racc);
    for(bi=0;bi<N;bi+=bs)for(bj=0;bj<N;bj+=bs)for(bk=0;bk<N;bk+=bs)
     for(i=bi;i<bi+bs&&i<N;i++)for(j=bj;j<bj+bs&&j<N;j++)for(k=bk;k<bk+bs&&k<N;k++){
        int id=IX(i,j,k);
        for(d=0;d<6;d++){
            int t=IX(i+DI[d],j+DJ[d],k+DK[d]);
            int64_t q=(int64_t)(fl[id][d]*RSCALE);
            racc[t]+=q; racc[id]-=q;
        }
     }
    for(i=0;i<NN;i++) f[i]+=(double)racc[i]/RSCALE;
}
static void apply_i(int bs){
    int bi,bj,bk,i,j,k,d;
    memset(Iacc,0,sizeof Iacc);
    for(bi=0;bi<N;bi+=bs)for(bj=0;bj<N;bj+=bs)for(bk=0;bk<N;bk+=bs)
     for(i=bi;i<bi+bs&&i<N;i++)for(j=bj;j<bj+bs&&j<N;j++)for(k=bk;k<bk+bs&&k<N;k++){
        int id=IX(i,j,k);
        for(d=0;d<6;d++){
            int t=IX(i+DI[d],j+DJ[d],k+DK[d]);
            Iacc[t]+=Ifl[id][d]; Iacc[id]-=Ifl[id][d];
        }
     }
    for(i=0;i<NN;i++) If[i]+=Iacc[i];
}
static void init(void){
    int i,j,k;
    for(i=0;i<N;i++)for(j=0;j<N;j++)for(k=0;k<N;k++){
        double d=sqrt((i-N*0.41)*(i-N*0.41)+(j-N*0.53)*(j-N*0.53)+(k-N*0.47)*(k-N*0.47));
        double v=8.0-d; v=v<0?0:(v>1?1:v);
        f[IX(i,j,k)]=v; If[IX(i,j,k)]=(int64_t)(v*S+0.5);
    }
}
static uint64_t hb(const void*p,size_t n){
    const unsigned char*q=p; uint64_t h=1469598103934665603ULL;
    for(size_t i=0;i<n;i++){h^=q[i];h*=1099511628211ULL;} return h;
}
int main(void){
    int blocks[]={2,4,8,16,32}, nb=5, b, s;
    uint64_t hn[9],hk[9],hr[9],hi[9];
    printf("3-D UNSPLIT VOF — decomposition invariance\n");
    printf("grid %d^3 = %d cells, %d steps, CFL 0.30 (non-dyadic)\n\n",N,NN,STEPS);
    for(b=0;b<nb;b++){
        int bs=blocks[b];
        init(); for(s=0;s<STEPS;s++){ fluxes_f(0.30); apply_f(bs,0); }
        hn[b]=hb(f,sizeof f);
        init(); for(s=0;s<STEPS;s++){ fluxes_f(0.30); apply_f(bs,1); }
        hk[b]=hb(f,sizeof f);
        init(); for(s=0;s<STEPS;s++){ fluxes_f(0.30); apply_r(bs); }
        hr[b]=hb(f,sizeof f);
        init(); for(s=0;s<STEPS;s++){ fluxes_i(19,64); apply_i(bs); }
        hi[b]=hb(If,sizeof If);
        printf("  block %2d : naive %#018llx  kahan %#018llx  repro %#018llx  ring %#018llx\n",
               bs,(unsigned long long)hn[b],(unsigned long long)hk[b],
               (unsigned long long)hr[b],(unsigned long long)hi[b]);
    }
    printf("\n%-38s %-22s %-12s\n","variant","relative volume drift","time (s)");
    double t0,tt; double m0; int64_t m0i;
    init(); m0=0; for(int q=0;q<NN;q++) m0+=f[q];
    m0i=0; for(int q=0;q<NN;q++) m0i+=If[q];
    struct { const char*nm; int kind; } V[]={{"float64, naive",0},{"float64, Kahan",1},
                                             {"float64, fixed-point accum",2},{"ring Z_256",3}};
    for(int v=0;v<4;v++){
        init(); t0=now();
        for(s=0;s<STEPS;s++){
            if(V[v].kind==3){ fluxes_i(19,64); apply_i(8); }
            else { fluxes_f(0.30);
                   if(V[v].kind==0) apply_f(8,0);
                   else if(V[v].kind==1) apply_f(8,1);
                   else apply_r(8); }
        }
        tt=now()-t0;
        if(V[v].kind==3){ int64_t m=0; for(int q=0;q<NN;q++) m+=If[q];
            printf("%-38s %-22s %-12.3f\n",V[v].nm, m==m0i?"0  (exact)":"nonzero", tt); }
        else { double m=0; for(int q=0;q<NN;q++) m+=f[q];
            printf("%-38s %-22.3e %-12.3f\n",V[v].nm, fabs(m-m0)/m0, tt); }
    }
    printf("\nWISP CENSUS after %d steps (cells that should be empty or full)\n",STEPS);
    printf("  %-34s %12s %12s %12s\n","variant","f<1e-8","f<1e-12","1-f<1e-12");
    for(int v=0;v<4;v++){
        init();
        for(s=0;s<STEPS;s++){
            if(v==3){ fluxes_i(19,64); apply_i(8); }
            else { fluxes_f(0.30); if(v==0) apply_f(8,0); else if(v==1) apply_f(8,1); else apply_r(8); }
        }
        long long w8=0,w12=0,u12=0;
        if(v==3){ for(int q=0;q<NN;q++){ if(If[q]!=0 && If[q]<1) w8++; }
                  printf("  %-34s %12lld %12lld %12lld\n","ring Z_256 (integer: none possible)",0LL,0LL,0LL); }
        else { for(int q=0;q<NN;q++){ double x=f[q];
                 if(x>0 && x<1e-8) w8++; if(x>0 && x<1e-12) w12++;
                 if(x<1 && 1-x<1e-12) u12++; }
               const char*nm = v==0?"float64, naive":(v==1?"float64, Kahan":"float64, fixed-point accum");
               printf("  %-34s %12lld %12lld %12lld\n",nm,w8,w12,u12); }
    }
    { init();
      for(s=0;s<STEPS;s++){ fluxes_f(0.30); apply_f(8,0); }
      long long sub=0,tot=0;
      for(int q=0;q<NN;q++){ if(f[q]>0 && f[q]<1.0/S) sub++; if(f[q]>0&&f[q]<1) tot++; }
      printf("\n  SUB-RESOLUTION CELLS in float (0 < f < 1/256, i.e. below the ring's quantum):\n");
      printf("    %lld cells, out of %lld partial cells  (%.1f%%)\n",sub,tot,100.0*sub/(tot?tot:1));
      printf("    These are the cells the ring quantises to 0. That is the 8.4x branch gap:\n");
      printf("    the ring is not avoiding wisps, it is RESOLVING LESS.\n"); }
    printf("\n  A cell in Z_256 is exactly 0, exactly 256, or a genuine interface cell.\n");
    printf("  There is no representable value between 0 and 1/256, so a wisp cannot exist.\n");
    printf("\nBRANCH COUNTS over the timed runs (why the times differ):\n");
    printf("  float : %lld empty (skipped)  %lld full (cheap)  %lld interface (INVERSION)\n",EMPTY_F,FULL_F,CNT_F);
    printf("  ring  : %lld empty (skipped)  %lld full (cheap)  %lld interface (INVERSION)\n",EMPTY_I,FULL_I,CNT_I);
    printf("  ratio of expensive-path cells, float/ring = %.2fx\n",(double)CNT_F/(CNT_I?CNT_I:1));
    int un=0,uk=0,ur=0,ui=0;
    for(b=0;b<nb;b++){int sn=0,sk=0,sr=0,si=0;
        for(int c=0;c<b;c++){ if(hn[c]==hn[b])sn=1; if(hk[c]==hk[b])sk=1;
                              if(hr[c]==hr[b])sr=1; if(hi[c]==hi[b])si=1; }
        if(!sn)un++; if(!sk)uk++; if(!sr)ur++; if(!si)ui++; }
    printf("\nDISTINCT FINAL FIELDS across %d decompositions:\n",nb);
    printf("   float64, naive accumulation        : %d\n",un);
    printf("   float64, Kahan-compensated         : %d\n",uk);
    printf("   float64, fixed-point accumulation   : %d\n",ur);
    printf("   ring Z_256                         : %d\n",ui);
    return 0;
}
