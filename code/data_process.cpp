#include <iostream>
#include <fstream>
#include <cstdlib>
#include <cmath>
#include <string.h>

using namespace std;

void generate_input();
int run_number=0;




int main(){

    cout<<"run nunber:";
    scanf("%d", &run_number);
    generate_input();
    system("chmod 777 one_shot");
    system("./one_shot");

}



void generate_input()
{
    ofstream dataprocess;
    dataprocess.open("one_shot");
    dataprocess<<"MakeTagList -b 3 -r "<<run_number<<" -det 'MPCCD-1N0-M01-002, MPCCD-1N0-M01-003, MPCCD-8-2-002' -out tag_"<<run_number<<".list"<<endl;
    dataprocess<<"DataConvert4 -l tag_"<<run_number<<".list -dir /UserData/fperakis/2016_6/run"<<run_number<<"/ -o "<<run_number<<".h5"<<endl;
    dataprocess<<"./matlab_bacground_exe"<<endl;
    dataprocess<<"./integ.out"<<endl;
    dataprocess<<"./av.out"<<endl;
}

    


