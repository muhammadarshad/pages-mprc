/* Decomposition reproducibility on the CORRECTED PLIC scheme.
 *
 * Model of a domain-decomposed parallel VOF solver: after each pair of
 * sweeps the solver applies the standard global mass-fixing step, which
 * needs a reduction over the whole grid.  In a parallel run that reduction
 * is a tree over sub-blocks, so its summation order is set by the
 * decomposition.  Float64 addition is not associative -> the correction
 * differs at the ulp level -> the trajectories separate.
 * Ring: the reduction is an exact integer sum (associative), and the
 * correction is an integer redistribution in a fixed scan order, so every
 * decomposition produces the bit-identical field.
 * Build: gcc -O2 -o repro_vof repro_vof.c -lm                              */
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>
#include <stdint.h>
#define N 128
#define S 256
static double f[N*N],flx[N*N],scr[N*N];
static int64_t F[N*N]; static double Flx[N*N]; static int64_t scrI[N*N];
#define ID(i,j) ((((i)+N)%N)*N + (((j)+N)%N))
static double area_pos(double a,double b,double c){double m,M,t,s=a+b;
 if(s<1e-15)return c>0?1:0; a/=s;b/=s;c/=s;
 if(c<=0)return 0; if(c>=1)return 1;
 if(a<b){m=a;M=b;}else{m=b;M=a;}
 if(m<1e-15)return c/M<1?c/M:1;
 if(c<=m)return c*c/(2*a*b);
 if(c<=M)return (2*c-m)/(2*M);
 t=1-c; return 1-t*t/(2*a*b);}
static double area_s(double a,double b,double c){
 double cc=c-(a<0?a:0)-(b<0?b:0); return area_pos(fabs(a),fabs(b),cc);}
static double inv_s(double a,double b,double t){double lo=-2,hi=2,m;int i;
 for(i=0;i<60;i++){m=.5*(lo+hi); if(area_s(a,b,m)<t)lo=m; else hi=m;} return .5*(lo+hi);}
static double flux_R(double a,double b,double c,double d){
 if(d<=0)return 0; return d*area_s(a*d,b,c-a*(1.0-d));}
static double flux_L(double a,double b,double c,double d){
 if(d<=0)return 0; return d*area_s(a*d,b,c);}
static double Tper=2.0;
static double uvel(double x,double y,double t){return -sin(M_PI*x)*sin(M_PI*x)*sin(2*M_PI*y)*cos(M_PI*t/Tper);}
static double vvel(double x,double y,double t){return  sin(2*M_PI*x)*sin(M_PI*y)*sin(M_PI*y)*cos(M_PI*t/Tper);}
static double fv_(int i,int j,int ax,double t){double h=1.0/N;
 return ax? uvel(j*h,(i+0.5)*h,t) : vvel((j+0.5)*h,i*h,t);}
#define YOUNG(A,ii,jj,gx,gy) \
 gx=-((A[ID(ii-1,jj+1)]+2*A[ID(ii,jj+1)]+A[ID(ii+1,jj+1)]) \
    -(A[ID(ii-1,jj-1)]+2*A[ID(ii,jj-1)]+A[ID(ii+1,jj-1)]))/8.0; \
 gy=-((A[ID(ii+1,jj-1)]+2*A[ID(ii+1,jj)]+A[ID(ii+1,jj+1)]) \
    -(A[ID(ii-1,jj-1)]+2*A[ID(ii-1,jj)]+A[ID(ii-1,jj+1)]))/8.0;
static void sweep_f(double t,double dt,int ax,int first){int i,j;double h=1.0/N;
 for(i=0;i<N;i++)for(j=0;j<N;j++){double d,v,gx,gy,s2,a,b,al,A;int di,dj,ii,jj;
  d=fv_(i,j,ax,t)*dt/h; di=ax?0:-1; dj=ax?-1:0;
  if(d>=0){ii=(((i+di)%N)+N)%N; jj=(((j+dj)%N)+N)%N;}else{ii=i;jj=j;}
  v=f[ID(ii,jj)];
  if(v<=1e-14){flx[ID(i,j)]=0;continue;}
  if(v>=1-1e-14){flx[ID(i,j)]=d;continue;}
  YOUNG(f,ii,jj,gx,gy)
  s2=fabs(gx)+fabs(gy); if(s2<1e-14){flx[ID(i,j)]=v*d;continue;}
  gx/=s2;gy/=s2; a=ax?gx:gy; b=ax?gy:gx; al=inv_s(a,b,v);
  A=(d>=0)?flux_R(a,b,al,d):flux_L(a,b,al,-d);
  if(A<0)A=0; if(A>v)A=v; flx[ID(i,j)]=(d>=0)?A:-A;}
 for(i=0;i<N;i++)for(j=0;j<N;j++){
  double uL=fv_(i,j,ax,t), uR=ax?fv_(i,j+1,ax,t):fv_(i+1,j,ax,t);
  double div=(uR-uL)*dt/h, FL=flx[ID(i,j)], FR=ax?flx[ID(i,j+1)]:flx[ID(i+1,j)];
  double val=f[ID(i,j)]-(FR-FL);
  if(first)val=val/(1.0-div); else val=val+f[ID(i,j)]*div;
  scr[ID(i,j)]=val;}
 for(i=0;i<N*N;i++){f[i]=scr[i]; if(f[i]<0)f[i]=0; if(f[i]>1)f[i]=1;}}
static void sweep_i(double t,double dt,int ax,int first){int i,j;double h=1.0/N;
 for(i=0;i<N;i++)for(j=0;j<N;j++){double d,v,gx,gy,s2,a,b,al,A;int di,dj,ii,jj;
  d=fv_(i,j,ax,t)*dt/h; di=ax?0:-1; dj=ax?-1:0;
  if(d>=0){ii=(((i+di)%N)+N)%N; jj=(((j+dj)%N)+N)%N;}else{ii=i;jj=j;}
  v=(double)F[ID(ii,jj)]/S;
  if(F[ID(ii,jj)]<=0){Flx[ID(i,j)]=0;continue;}
  if(F[ID(ii,jj)]>=S){Flx[ID(i,j)]=d;continue;}
  YOUNG(F,ii,jj,gx,gy)
  s2=fabs(gx)+fabs(gy); if(s2<1e-14){Flx[ID(i,j)]=v*d;continue;}
  gx/=s2;gy/=s2; a=ax?gx:gy; b=ax?gy:gx; al=inv_s(a,b,v);
  A=(d>=0)?flux_R(a,b,al,d):flux_L(a,b,al,-d);
  if(A<0)A=0; if(A>v)A=v; Flx[ID(i,j)]=(d>=0)?A:-A;}
 for(i=0;i<N;i++)for(j=0;j<N;j++){
  double uL=fv_(i,j,ax,t), uR=ax?fv_(i,j+1,ax,t):fv_(i+1,j,ax,t);
  double div=(uR-uL)*dt/h, FL=Flx[ID(i,j)], FR=ax?Flx[ID(i,j+1)]:Flx[ID(i+1,j)];
  double val=(double)F[ID(i,j)]/S-(FR-FL);
  if(first)val=val/(1.0-div); else val=val+((double)F[ID(i,j)]/S)*div;
  scrI[ID(i,j)]=(int64_t)floor(val*S+0.5);}
 for(i=0;i<N*N;i++){F[i]=scrI[i]; if(F[i]<0)F[i]=0; if(F[i]>S)F[i]=S;}}
static double red_f(int bs){double tot=0;int bi,bj,i,j;
 for(bi=0;bi<N;bi+=bs)for(bj=0;bj<N;bj+=bs){double b=0;
  for(i=bi;i<bi+bs&&i<N;i++)for(j=bj;j<bj+bs&&j<N;j++)b+=f[i*N+j];
  tot+=b;} return tot;}
static int64_t red_i(int bs){int64_t tot=0;int bi,bj,i,j;
 for(bi=0;bi<N;bi+=bs)for(bj=0;bj<N;bj+=bs){int64_t b=0;
  for(i=bi;i<bi+bs&&i<N;i++)for(j=bj;j<bj+bs&&j<N;j++)b+=F[i*N+j];
  tot+=b;} return tot;}
static void init(void){int i,j,si,sj,K=16;double h=1.0/N;
 for(i=0;i<N;i++)for(j=0;j<N;j++){int in=0;
  for(si=0;si<K;si++)for(sj=0;sj<K;sj++){double x=(j+(sj+.5)/K)*h,y=(i+(si+.5)/K)*h;
   if(hypot(x-0.5,y-0.75)<0.15)in++;}
  double v=(double)in/(K*K); f[ID(i,j)]=v; F[ID(i,j)]=(int64_t)floor(v*S+0.5);}}
int main(void){
 int bss[]={1,2,4,8,16,32,64,128}, P=8, p, s;
 static double outF[8][N*N]; static int64_t outI[8][N*N];
 double h=1.0/N, dt=0.5*h; int steps=(int)(Tper/dt+0.5); dt=Tper/steps;
 double V0f=0; int64_t V0i=0;
 printf("Decomposition reproducibility, corrected PLIC, N=%d, %d steps, %d decompositions\n",N,steps,P);
 for(p=0;p<P;p++){
   int bs=bss[p];
   init();
   if(p==0){ V0f=red_f(bs); V0i=red_i(bs); }
   for(s=0;s<steps;s++){
     double tm=s*dt+0.5*dt; int ax=(s&1);
     sweep_f(tm,dt,ax,1); sweep_f(tm,dt,!ax,0);
     sweep_i(tm,dt,ax,1); sweep_i(tm,dt,!ax,0);
     {double V=red_f(bs); if(V>0){double r=V0f/V; for(int q=0;q<N*N;q++) f[q]*=r;}}
     {int64_t V=red_i(bs), D=V0i-V, q, step=(D>0)?1:-1;
      for(q=0;q<N*N && D!=0;q++){
        if(F[q]>0 && F[q]<S){ F[q]+=step; D-=step; }}}
   }
   memcpy(outF[p],f,sizeof f); memcpy(outI[p],F,sizeof F);
 }
 int df=1, di=1, seenF[8]={0}, seenI[8]={0};
 for(p=1;p<P;p++){ int newf=1,newi=1;
   for(int q=0;q<p;q++){ if(!memcmp(outF[p],outF[q],sizeof outF[0])) newf=0;
                         if(!memcmp(outI[p],outI[q],sizeof outI[0])) newi=0; }
   df+=newf; di+=newi; seenF[p]=newf; seenI[p]=newi; }
 double maxd=0; int64_t maxi=0;
 for(p=1;p<P;p++)for(int q=0;q<N*N;q++){
   double d=fabs(outF[p][q]-outF[0][q]); if(d>maxd)maxd=d;
   int64_t e=llabs(outI[p][q]-outI[0][q]); if(e>maxi)maxi=e; }
 printf("\n  float64  : %d distinct final fields out of %d   max |df| = %.3e\n",df,P,maxd);
 printf("  QH4 ring : %d distinct final fields out of %d   max |dF| = %lld level(s)\n",di,P,(long long)maxi);
 printf("\n  %s\n",(df>1&&di==1)?"RESULT: float64 is decomposition-dependent; the ring is bit-identical."
                                :"RESULT: no separation observed.");
 return 0;}
