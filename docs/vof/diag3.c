#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#define N 64
static double f[N*N],g[N*N],flx[N*N];
#define ID(i,j) (((i)+N)%N)*N + (((j)+N)%N)
static double area_pos(double a,double b,double c){double m,M,t,s=a+b;
 if(s<1e-15) return c>0?1:0; a/=s;b/=s;c/=s;
 if(c<=0)return 0; if(c>=1)return 1;
 if(a<b){m=a;M=b;}else{m=b;M=a;}
 if(m<1e-15) return c/M<1?c/M:1;
 if(c<=m) return c*c/(2*a*b);
 if(c<=M) return (2*c-m)/(2*M);
 t=1-c;   return 1-t*t/(2*a*b);}
static double area_s(double a,double b,double c){
 double cc=c - (a<0?a:0) - (b<0?b:0);
 return area_pos(fabs(a),fabs(b),cc);}
static double inv_s(double a,double b,double t){double lo=-2,hi=2,m;int i;
 for(i=0;i<60;i++){m=.5*(lo+hi); if(area_s(a,b,m)<t) lo=m; else hi=m;} return .5*(lo+hi);}
static double flux_R(double a,double b,double c,double d){
 if(d<=0)return 0; return d*area_s(a*d, b, c - a*(1.0-d));}
static double flux_L(double a,double b,double c,double d){
 if(d<=0)return 0; return d*area_s(a*d, b, c);}
static double vol(void){double s=0;for(int q=0;q<N*N;q++)s+=f[q];return s/(N*N);}
static double mx(void){double s=0;for(int q=0;q<N*N;q++)if(f[q]>s)s=f[q];return s;}
int main(void){
 double h=1.0/N;
 for(int i=0;i<N;i++)for(int j=0;j<N;j++){int in=0;
   for(int a=0;a<8;a++)for(int b=0;b<8;b++){double x=(j+(b+.5)/8)*h,y=(i+(a+.5)/8)*h;
     if(hypot(x-0.5,y-0.75)<0.15)in++;}
   f[ID(i,j)]=in/64.0;}
 double v0=vol();
 printf("initial volume %.8f  max %.4f\n",v0,mx());
 printf("\nSIGNED normal, corrected flux, pure translation u=+1, one period:\n");
 double d=0.5; int steps=(int)(1.0/(d*h)+0.5);
 for(int s=0;s<steps;s++){
   for(int i=0;i<N;i++)for(int j=0;j<N;j++){
     double v=f[ID(i,j)],gx,gy,s2,a,A;
     if(v<=1e-14){flx[ID(i,j)]=0;continue;}
     if(v>=1-1e-14){flx[ID(i,j)]=d;continue;}
     gx=-(f[ID(i,j+1)]-f[ID(i,j-1)])*0.5; gy=-(f[ID(i+1,j)]-f[ID(i-1,j)])*0.5;
     s2=fabs(gx)+fabs(gy); if(s2<1e-14){flx[ID(i,j)]=v*d;continue;}
     gx/=s2; gy/=s2;
     a=inv_s(gx,gy,v);
     A=flux_R(gx,gy,a,d);
     if(A<0)A=0; if(A>v)A=v;
     flx[ID(i,j)]=A;
   }
   for(int i=0;i<N;i++)for(int j=0;j<N;j++)
     g[ID(i,j)]=f[ID(i,j)]-flx[ID(i,j)]+flx[ID(i,j-1)];
   for(int q=0;q<N*N;q++) f[q]=g[q];
 }
 double e=0;
 for(int i=0;i<N;i++)for(int j=0;j<N;j++){int in=0;
   for(int a=0;a<8;a++)for(int b=0;b<8;b++){double x=(j+(b+.5)/8)*h,y=(i+(a+.5)/8)*h;
     if(hypot(x-0.5,y-0.75)<0.15)in++;}
   e+=fabs(f[ID(i,j)]-in/64.0)*h*h;}
 printf("  after %d steps: volume %.8f  drift %.2e  max %.4f\n",steps,vol(),fabs(vol()-v0),mx());
 printf("  E1 vs exact: %.4e\n",e);
 printf("\n  %s\n", (fabs(vol()-v0)<1e-12 && e<5e-3)?"PASS":"still smearing");
 return 0;}
