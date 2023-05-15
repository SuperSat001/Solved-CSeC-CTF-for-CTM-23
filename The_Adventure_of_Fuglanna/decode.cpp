#include "bits/stdc++.h"
using namespace std;
#define out(x) cout<<x<<"\n"
#define watch(x) cerr<<(#x)<<" is "<<x<<"\n";
#define vout(x) for(auto i : x)cout<<i;
#define rep(i,n) for(int i(0); i<n; i++)
#define vi vector<int>
#define pb push_back

void reverseKeys(int keys[], int rkeys[]){
	rep(i,8)rkeys[keys[i]] = i;
}

void decode(char arr[], char decoded[], int n, int rkeys[], int iv){
	int acc;
	for(int i = n-1; i > 0; i--){
		acc = 0;
	    for( int j = 0; j < 8; j++){
	      int b = (arr[i] >> j) & 1;
	      acc |= (b << rkeys[j]);
	    }
	    acc ^= arr[i-1];
	    decoded[i] = acc;
	}

	acc = 0;
    for( int j = 0; j < 8; j++){
      int b = (arr[0] >> j) & 1;
      acc |= (b << rkeys[j]);
    }
    acc ^= iv;
    decoded[0] = acc;
}

int fact(int n){
    return (n==0) || (n==1) ? 1 : n*fact(n-1);
}

int main(){

	int n, x; cin>>n;
	char arr[n];
	rep(i,n){
		cin>>x;
		arr[i] = x;
	}

	int keys[8] = {0, 1, 2, 3, 4, 5, 6, 7};
	int rkeys[8];
	//vout(rkeys);

	char decoded1[n], decoded2[n];
    //vout(decoded);

	rep(i, fact(8)){
		reverseKeys(keys, rkeys);
		decode(arr, decoded1, n, rkeys, 0);
		rep(k, 256){
			decode(decoded1, decoded2, n, rkeys, k);
			vout(keys);
			cout<<" "<<k<<" ";
			vout(decoded2);
			cout<<"\n";
		}

		next_permutation(keys, keys+8);
	}


	return 0;

}