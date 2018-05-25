#include<iostream>
#include "atlimage.h"
#include<string>
#include<vector>
#include<io.h>
#include"color.h"
#include"Windows.h"
#include <fstream>  
#include <sstream>  
#include "math.h"
#include"colorhistogram_HSV.h"
using namespace std;

int colorhistogram_HSV()
{
	cout << "������HSV��ɫֱ��ͼ��ά��(������ż��)��";
	int dimensionality;
	cin >> dimensionality;
	while (dimensionality % 2 != 0)
	{
		cout << "�����ά�Ȳ�Ϊż�������������룺";
		cin >> dimensionality;
	}

	ifstream infile("image/imagelist.txt");
	ofstream outfile;
	outfile.open("colorhistogram_HSV.csv", wios::out);
	//outfile.imbue(std::locale("chs"));
	string image_name;
	int count = 0;

	while (!infile.eof())
	{
		getline(infile, image_name);

		/*��ͼƬ���д���*/
		CImage image;
		int iHeight, iWidth;
		BYTE byte[3];//˳������Ϊ��byteR, byteG, byteB
		double R,G,B;
		double maxbyte, minbyte;
		
		string image_path = "image\\" + image_name;
		LPCTSTR image_path_str = _T(image_path.c_str());
		image.Load(image_path_str);

		iHeight = image.GetHeight();
		iWidth = image.GetWidth();

		//int RedDis = 0, GreenDis = 0, YellowDis = 0, GreyDis = 0, BlueDis = 0, WhiteDis = 0, CyanDis = 0, PurpleDis = 0;
		//int RedNumber = 0, GreenNumber = 0, YellowNumber = 0, GreyNumber = 0, BlueNumber = 0, WhiteNumber = 0, CyanNumber = 0, PurpleNumber = 0;
		double *colors=new double[dimensionality]();
		//memset(colors, 0.0, sizeof(colors));

		for (int iRow = 0; iRow < iWidth; iRow++)
			for (int iCol = 0; iCol < iHeight; iCol++)
			{
				COLORREF colorref = image.GetPixel(iRow, iCol);
				if (colorref == CLR_INVALID)
				{
					cout << "Out of range!";
					continue;
				}

				byte[0] = GetRValue(colorref);
				byte[1] = GetGValue(colorref);
				byte[2] = GetBValue(colorref);

				//�ĵ�Ҫ�������������ʽ������ά��������
				R = byte[0] & 0xFF;//��BYTEת����double
				G = byte[1] & 0xFF;
				B = byte[2] & 0xFF;

				if (R >= G)
				{
					maxbyte = R;
					minbyte = G;
				}
				else
				{
					maxbyte = G;
					minbyte = R;
				}
				if (maxbyte <= B)
					maxbyte = B;
				if (minbyte >= B)
					minbyte = B;

				double H, S, V;
				double difference;
				V = maxbyte;
				//ȷ��H
				difference = maxbyte - minbyte;
				if (difference == 0)
					H = 0;
				else if (maxbyte == R && G >= B)
					H = 60 * (G - B) / difference;
				else if (maxbyte == R && G < B)
					H = 60 * (G - B) / difference + 360.0;
				else if (maxbyte == G)
					H = 60 * (B - R) / difference + 120.0;
				else if (maxbyte == B)
					H = 60 * (R - G) / difference + 240.0;
				//ȷ��S
				if (maxbyte == 0)
					S = 0;
				else
					S = 1 - minbyte / maxbyte;

				int basie =ceil( 360 / (dimensionality / 2));
				
				//��HSV���з���
				int h=ceil(H / basie);
				if (h == 0)
					h = h + 1;//���ǵ�0�����������i��1��ʼ
				int j;
				if (S > 0.5)
					j = 1;
				else j = 0;
				colors[(h - 1) + j * (dimensionality/2)]++;				
			}

		//�ѽ��д���ļ���		
		outfile << image_name << ":" << ",";
		for (int i = 0; i <	dimensionality; i++)
		{
			if (i != dimensionality-1)
				outfile << (int)(((double)colors[i] / (double)(iHeight*iWidth)) * 10000) << ",";
			else
				outfile << (int)(((double)colors[i] / (double)(iHeight*iWidth)) * 10000) << "\n";
		}

		cout << count << endl;
		count = count + 1;

		image.GetBits();
		image.Destroy();
		delete colors;
	}
	infile.close();
	outfile.close();
	return 0;
}			