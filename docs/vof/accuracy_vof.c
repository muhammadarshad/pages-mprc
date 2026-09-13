/* Rider-Kothe reversed single vortex: the standard VOF accuracy benchmark.
 * The flow reverses at T/2, so the exact field at t=T is the initial field.
 * Any deviation is error.  float64 PLIC vs QH4-ring (256-level) PLIC.
 *
 * Geometry kernel: signed-normal PLIC (area_s / inv_s / flux_R / flux_L),
 * validated against pure translation (volume drift 0, E1 = 1.09e-3, N=64).
 * Build: gcc -O2 -o accuracy_vof accuracy_vof.c -lm                        */
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <stdint.h>

static int S = 256;               /* ring levels: f in {0..S}/S           */
static int N;
static double *f,*f0,*flx;
static int64_t *F,*F0;
static double  *Flx;                /* ring flux held as k/S               */
#define ID(i,j) ((((i)+N)%N)*N + (((j)+N)%N))

/* ---- fraction of the unit cell with |a|X+|b|Y <= c,  a,b >= 0 ---------- */
static double area_pos(double a,double b,double c){
    double m,M,t,s=a+b;
    if(s<1e-15) return c>0?1.0:0.0;
    a/=s; b/=s; c/=s;
    if(c<=0) return 0.0; if(c>=1) return 1.0;
    if(a<b){m=a;M=b;} else {m=b;M=a;}
    if(m<1e-15) return c/M<1.0? c/M : 1.0;
    if(c<=m) return c*c/(2*a*b);
    if(c<=M) return (2*c-m)/(2*M);
    t=1-c;   return 1-t*t/(2*a*b);
}
/* ---- SIGNED normal: fraction of {aX+bY <= c}. Reflect each negative axis */
static double area_s(double a,double b,double c){
    double cc = c - (a<0?a:0) - (b<0?b:0);
    return area_pos(fabs(a),fabs(b),cc);
}
static double inv_s(double a,double b,double t){
    double lo=-2,hi=2,m; int i;
    for(i=0;i<60;i++){ m=.5*(lo+hi); if(area_s(a,b,m)<t) lo=m; else hi=m; }
    return .5*(lo+hi);
}
/* flux through the X=1 face over width d  (strip X in [1-d,1])            */
static double flux_R(double a,double b,double c,double d){
    if(d<=0) return 0.0; return d*area_s(a*d, b, c - a*(1.0-d));
}
/* flux through the X=0 face over width d  (strip X in [0,d])              */
static double flux_L(double a,double b,double c,double d){
    if(d<=0) return 0.0; return d*area_s(a*d, b, c);
}
/* ---- Rider-Kothe single vortex, reversed by cos(pi t / T) -------------- */
static double Tper;
static double uvel(double x,double y,double t){
    return -sin(M_PI*x)*sin(M_PI*x)*sin(2*M_PI*y)*cos(M_PI*t/Tper);
}
static double vvel(double x,double y,double t){
    return  sin(2*M_PI*x)*sin(M_PI*y)*sin(M_PI*y)*cos(M_PI*t/Tper);
}
/* face velocity on the lower/left face of cell (i,j); axis 1 = x, 0 = y   */
static double face_vel(int i,int j,int axis,double t){
    double h=1.0/N;
    return axis ? uvel(j*h,(i+0.5)*h,t) : vvel((j+0.5)*h,i*h,t);
}
/* ---- one directional sweep, float64 ------------------------------------ */
/* first==1 -> dilation form (divide by 1-div); first==0 -> compression add */
static void sweep_f(double t,double dt,int axis,int first){
    int i,j; double h=1.0/N;
    for(i=0;i<N;i++)for(j=0;j<N;j++){
        double d,v,gx,gy,s2,a,b,al,A;
        int di,dj,ii,jj;
        d = face_vel(i,j,axis,t)*dt/h;
        di = axis? 0 : -1;  dj = axis? -1 : 0;      /* upwind donor offset */
        if(d>=0){ ii=(((i+di)%N)+N)%N; jj=(((j+dj)%N)+N)%N; }
        else    { ii=i; jj=j; }
        v = f[ID(ii,jj)];
        if(v<=1e-14){ flx[ID(i,j)]=0; continue; }
        if(v>=1-1e-14){ flx[ID(i,j)]=d; continue; }
        gx = -((f[ID(ii-1,jj+1)]+2*f[ID(ii,jj+1)]+f[ID(ii+1,jj+1)])
              -(f[ID(ii-1,jj-1)]+2*f[ID(ii,jj-1)]+f[ID(ii+1,jj-1)]))/8.0;
        gy = -((f[ID(ii+1,jj-1)]+2*f[ID(ii+1,jj)]+f[ID(ii+1,jj+1)])
              -(f[ID(ii-1,jj-1)]+2*f[ID(ii-1,jj)]+f[ID(ii-1,jj+1)]))/8.0;
        s2 = fabs(gx)+fabs(gy);
        if(s2<1e-14){ flx[ID(i,j)] = v*d; continue; }
        gx/=s2; gy/=s2;                              /* signed, L1-normal  */
        a = axis? gx : gy;                            /* along sweep axis  */
        b = axis? gy : gx;
        al = inv_s(a,b,v);
        A = (d>=0)? flux_R(a,b,al, d) : flux_L(a,b,al,-d);
        if(A<0)A=0; if(A>v)A=v;
        flx[ID(i,j)] = (d>=0)? A : -A;
    }
    for(i=0;i<N;i++)for(j=0;j<N;j++){
        double uL = face_vel(i,j,axis,t);
        double uR = axis? face_vel(i,j+1,axis,t) : face_vel(i+1,j,axis,t);
        double div = (uR-uL)*dt/h;
        double FL = flx[ID(i,j)];
        double FR = axis? flx[ID(i,j+1)] : flx[ID(i+1,j)];
        double val = f[ID(i,j)] - (FR-FL);
        if(first) val = val/(1.0-div);
        else      val = val + f[ID(i,j)]*div;
        f0[N*N+ID(i,j)] = val;
    }
    for(i=0;i<N*N;i++){ f[i]=f0[N*N+i]; if(f[i]<0)f[i]=0; if(f[i]>1)f[i]=1; }
}
/* ---- one directional sweep, QH4 ring (fixed point, S levels) ----------- */
static void sweep_i(double t,double dt,int axis,int first){
    int i,j; double h=1.0/N;
    for(i=0;i<N;i++)for(j=0;j<N;j++){
        double d,v,gx,gy,s2,a,b,al,A;
        int di,dj,ii,jj;
        d = face_vel(i,j,axis,t)*dt/h;
        di = axis? 0 : -1;  dj = axis? -1 : 0;
        if(d>=0){ ii=(((i+di)%N)+N)%N; jj=(((j+dj)%N)+N)%N; }
        else    { ii=i; jj=j; }
        v = (double)F[ID(ii,jj)]/S;
        if(F[ID(ii,jj)]<=0){ Flx[ID(i,j)]=0; continue; }
        if(F[ID(ii,jj)]>=S){ Flx[ID(i,j)]=d; continue; }
        gx = -(double)((F[ID(ii-1,jj+1)]+2*F[ID(ii,jj+1)]+F[ID(ii+1,jj+1)])
                      -(F[ID(ii-1,jj-1)]+2*F[ID(ii,jj-1)]+F[ID(ii+1,jj-1)]));
        gy = -(double)((F[ID(ii+1,jj-1)]+2*F[ID(ii+1,jj)]+F[ID(ii+1,jj+1)])
                      -(F[ID(ii-1,jj-1)]+2*F[ID(ii-1,jj)]+F[ID(ii-1,jj+1)]));
        s2 = fabs(gx)+fabs(gy);
        if(s2<1e-14){ Flx[ID(i,j)] = v*d; continue; }
        gx/=s2; gy/=s2;
        a = axis? gx : gy;
        b = axis? gy : gx;
        al = inv_s(a,b,v);
        A = (d>=0)? flux_R(a,b,al, d) : flux_L(a,b,al,-d);
        if(A<0)A=0; if(A>v)A=v;
        Flx[ID(i,j)] = (d>=0)? A : -A;
    }
    for(i=0;i<N;i++)for(j=0;j<N;j++){
        double uL = face_vel(i,j,axis,t);
        double uR = axis? face_vel(i,j+1,axis,t) : face_vel(i+1,j,axis,t);
        double div = (uR-uL)*dt/h;
        double FL = Flx[ID(i,j)];
        double FR = axis? Flx[ID(i,j+1)] : Flx[ID(i+1,j)];
        double val = (double)F[ID(i,j)]/S - (FR-FL);
        if(first) val = val/(1.0-div);
        else      val = val + ((double)F[ID(i,j)]/S)*div;
        F0[N*N+ID(i,j)] = (int64_t)floor(val*S+0.5);   /* quantise to ring */
    }
    for(i=0;i<N*N;i++){ F[i]=F0[N*N+i]; if(F[i]<0)F[i]=0; if(F[i]>S)F[i]=S; }
}
/* ---- initial condition: circle, sub-cell sampled ----------------------- */
static void init(double cx,double cy,double r){
    int i,j,si,sj,K=16; double h=1.0/N;
    for(i=0;i<N;i++)for(j=0;j<N;j++){
        int in=0;
        for(si=0;si<K;si++)for(sj=0;sj<K;sj++){
            double x=(j+(sj+0.5)/K)*h, y=(i+(si+0.5)/K)*h;
            if(hypot(x-cx,y-cy)<r) in++;
        }
        double v=(double)in/(K*K);
        f[ID(i,j)]=v; f0[ID(i,j)]=v;
        F[ID(i,j)]=(int64_t)floor(v*S+0.5); F0[ID(i,j)]=F[ID(i,j)];
    }
}
int main(int argc,char**argv){
    int res[]={32,64,128}, nr=3, k;
    Tper = (argc>1)? atof(argv[1]) : 2.0;
    if(argc>2) S = atoi(argv[2]);
    if(argc>3){ res[0]=atoi(argv[3]); nr=1; }
    printf("Rider-Kothe reversed single vortex, T = %.1f, CFL 0.5, Strang split, S = %d\n",Tper,S);
    printf("exact field at t=T is the initial field;  E1 = sum |f-f0| h^2\n\n");
    printf("%5s | %-12s %-6s | %-12s %-6s | %-9s | %-11s %-11s\n",
           "N","float64 E1","order","QH4 ring E1","order","ring/flt","dV float","dV ring");
    printf("------+---------------------+---------------------+-----------+------------------------\n");
    double pe=0,pi=0;
    for(k=0;k<nr;k++){
        N=res[k];
        f  = malloc(N*N*sizeof(double));
        f0 = malloc(2*N*N*sizeof(double));
        flx= malloc(N*N*sizeof(double));
        F  = malloc(N*N*sizeof(int64_t));
        F0 = malloc(2*N*N*sizeof(int64_t));
        Flx= malloc(N*N*sizeof(double));
        init(0.5,0.75,0.15);
        double h=1.0/N, dt=0.5*h, t=0, vf0=0, vi0=0;
        for(int q=0;q<N*N;q++){ vf0+=f0[q]; vi0+=(double)F0[q]/S; }
        int steps=(int)(Tper/dt+0.5); dt=Tper/steps;
        for(int s=0;s<steps;s++){
            double tm=t+0.5*dt;
            int ax = (s&1);                 /* Strang: alternate sweep order */
            sweep_f(tm,dt,ax,1);  sweep_f(tm,dt,!ax,0);
            sweep_i(tm,dt,ax,1);  sweep_i(tm,dt,!ax,0);
            t+=dt;
        }
        double ef=0,ei=0,vf=0,vi=0;
        for(int q=0;q<N*N;q++){
            ef += fabs(f[q]-f0[q])*h*h;
            ei += fabs((double)F[q]/S-(double)F0[q]/S)*h*h;
            vf += f[q]; vi += (double)F[q]/S;
        }
        char ob[16]="-", oc[16]="-";
        if(k){ snprintf(ob,16,"%.2f",log2(pe/ef)); snprintf(oc,16,"%.2f",log2(pi/ei)); }
        printf("%5d | %-12.4e %-6s | %-12.4e %-6s | %-9.3f | %-11.2e %-11.2e\n",
               N, ef, ob, ei, oc, ei/ef,
               fabs(vf-vf0)*h*h, fabs(vi-vi0)*h*h);
        pe=ef; pi=ei;
        free(f);free(f0);free(flx);free(F);free(F0);free(Flx);
    }
    return 0;
}
