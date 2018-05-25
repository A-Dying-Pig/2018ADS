// LoadImage.cpp : Defines the entry point for the console application.
//

#include<iostream>
#include "atlimage.h"
#include<string>
#include<vector>
#include<io.h>
#include"color.h"
#include"Windows.h"
#include <fstream>  
#include <sstream>  
#include"colorhistogram.h"
using namespace std;

int colorhistogram()
{		
	cout << "������RGB��ɫֱ��ͼ��ά�Ȼ���(����ά��Ϊ�������������)��";
	int dimensionality_base;
	cin >> dimensionality_base;
	int dimensionality = dimensionality_base * dimensionality_base*dimensionality_base;

	ifstream infile("image/imagelist.txt");
	ofstream outfile;
	outfile.open("colorhistogram.csv", wios::out);
	//outfile.imbue(std::locale("chs"));
	string image_name;
	int count = 0;

	while(!infile.eof())
	{
		getline(infile,image_name);
		
		/*��ͼƬ���д���*/
		CImage image;
		int iHeight, iWidth;
		BYTE byte[3];//˳������Ϊ��byteR, byteG, byteB
		int byte_int[3];
		int bin[3];
		
		string image_path="image\\"+image_name;
		LPCTSTR image_path_str = _T(image_path.c_str());
		image.Load(image_path_str);
	
		iHeight = image.GetHeight();
		iWidth = image.GetWidth();
		
		//int RedDis = 0, GreenDis = 0, YellowDis = 0, GreyDis = 0, BlueDis = 0, WhiteDis = 0, CyanDis = 0, PurpleDis = 0;
		//int RedNumber = 0, GreenNumber = 0, YellowNumber = 0, GreyNumber = 0, BlueNumber = 0, WhiteNumber = 0, CyanNumber = 0, PurpleNumber = 0;
		int *colors=new int[dimensionality]();
		//memset(colors, 0, sizeof(colors));

		for (int iRow = 0; iRow < iWidth; iRow++)
			for (int iCol = 0; iCol < iHeight; iCol++)
			{
				COLORREF colorref = image.GetPixel(iRow, iCol);
				if (colorref == CLR_INVALID)
				{
					cout<<"Out of range!";
					continue;
				}
				
				byte[0] = GetRValue(colorref);
				byte[1] = GetGValue(colorref);
				byte[2] = GetBValue(colorref);

				//�ĵ�Ҫ�������������ʽ������ά��������
				//ÿһά�����ֳ�dimensionality_base�Σ���dimensionality����ɫ����
				int basie = ceil(255 / dimensionality_base);

				for (int i = 0; i < 3; i++)//��Ӧ������ɫR,G,B
				{
					byte_int[i] = byte[i] & 0xFF;//��BYTEת����int	
					int h = ceil((double)byte_int[i]/ basie);
					if (h == 0)
						h = h + 1;//���ǵ�0�����������i��1��ʼ
					bin[i] = h - 1;							
				}
				int bin_number = bin[2] * dimensionality_base*dimensionality_base + bin[1] * dimensionality_base + bin[0];
				colors[bin_number] = colors[bin_number] + 1;	
			}

		//�ѽ��д���ļ���		
		outfile << image_path<<",";
		for (int i = 0; i < dimensionality; i++)
		{
			if (i != dimensionality-1)
				outfile << (int)(((double)colors[i] / (double)(iHeight*iWidth))* 10000) << ",";
			else
				outfile << (int)(((double)colors[i] / (double)(iHeight*iWidth))* 10000) << "\n";
		}

		cout << count << endl;
		count = count + 1;
		
		image.GetBits();
		image.Destroy();
		delete []colors;
	}	
	infile.close();
	outfile.close();
	return 0;		
}