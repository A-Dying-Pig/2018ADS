// LoadImage.cpp : Defines the entry point for the console application.
//

#include "stdafx.h"
#include <string>
#include "atlimage.h"
#include <windows.h>
#include <io.h>
#include <vector>
#include <fstream>
#include <iostream>
using namespace std;


bool get_filelist_from_dir(string path, vector<string>& files)
{
	long   hFile = 0;
	struct _finddata_t fileinfo;
	files.clear();
	if ((hFile = _findfirst(path.c_str(), &fileinfo)) != -1)
	{
		do
		{
			if (!(fileinfo.attrib &  _A_SUBDIR)) 
				files.push_back(fileinfo.name);
		} while (_findnext(hFile, &fileinfo) == 0);
		_findclose(hFile);
		return true;
	}
	else
		return false;
}

int texture( )
{
	string file_path = "image\\";
	string search_path = file_path +"*.JPEG";
	vector<string> file_list;
	if (!get_filelist_from_dir(search_path, file_list))
		cout << "open file error!" << endl;

	cout << file_list.size() << endl;
	ofstream m_out("texture.txt");

	for (int i = 0; i < file_list.size(); i++)
{	
	int iHeight, iWidth;
	BYTE byteR, byteG, byteB;
	int texture[256]={},order[8];
	for (int i = 0; i< 256; i++)
		texture[i] = 0;

	CImage image;
	string image_path = file_path + file_list[i];
	image.Load( _T(image_path.c_str()) );

	iHeight = image.GetHeight();
	iWidth = image.GetWidth();
	int *grey = new int[iHeight * iWidth];

	//cout<<file_list[i];
	//grey-map
	for ( int iRow = 0; iRow < iWidth; iRow++)
		for ( int iCol = 0; iCol < iHeight; iCol++ )
		{
			COLORREF colorref = image.GetPixel( iRow, iCol );

			if ( colorref==CLR_INVALID )
			{
				printf("Out of range!");
				continue;
			}

			byteR =  GetRValue( colorref );
			byteG =  GetGValue( colorref );
			byteB =  GetBValue( colorref );
			
			
			//weighted method to know the grey value
			grey[iCol * iWidth + iRow] = 0.3 * (unsigned int)byteR + 0.59 * (unsigned int)byteG + 0.11 * (unsigned int)byteB;
			//cout<<grey[iCol * iWidth + iRow]<<"\t";
			//printf("%Pixel at (%d,%d) RGB(%d,%d,%d) grey value is: %d \n",iRow,iCol,byteR,byteG,byteB,grey[iRow * iWidth + iCol]);			
		}
	int count = 0;
	//texture value
	for ( int iRow = 1; iRow < iWidth - 1; iRow++)
		for ( int iCol = 1; iCol < iHeight - 1; iCol++ )
		{
			count = 0;
			for (int p = -1; p <= 1; p++)
				for (int k = -1; k <= 1; k++)
				{
					if (p == 0 && k == 0)	continue;
					if (grey[(iCol + p) * iWidth + iRow + k] < grey[iCol * iWidth + iRow])
						order[count] = 0;
					else
						order[count] = 1;
					count++;
				}
			int id = order[0]*128 + order[1]*64 + order[2]*32 + order[3]*16 + order[4]*8 + order[5]*4 +order[6]*2 + order[7];
			//cout<<id<<endl;
			//cout<<id<<"\t"<<texture[id]<<endl;
			//if (id!=255) cout<<id<<"\t";
			texture[id]++;
		}
	//output
	count = (iHeight - 2) * (iWidth - 2);
	m_out << file_list[i]<<":"<<",";
	for (int j = 0; j < 256; j++)
	{
		if (j == 255) 
			m_out<<(double)texture[j]/(double)count <<endl;
		else 
			m_out<<(double)texture[j]/(double)count<<","; 
	}
	
	cout<<file_list[i]<<i<<"has been analysed!"<<endl;
	delete []grey;
	image.GetBits();
	image.Destroy();
}
	return 0;
}

int main()
{
	texture();
	return 0;
}