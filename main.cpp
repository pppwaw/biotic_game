#include<Arduino.h>
#define JSX A0
#define JSY A1
#define U 5
#define D 6
#define L 10
#define R 9

const double Alpha=0.01;
const int eps=10;
void setup()
{
	pinMode(JSX,INPUT);
	pinMode(JSY,INPUT);
	pinMode(U,OUTPUT);
	pinMode(D,OUTPUT);
	pinMode(L,OUTPUT);
	pinMode(R,OUTPUT);

	Serial.begin(9600);
}

void loop()
{
	int vx=analogRead(JSX);//492
	int vy=analogRead(JSY);//518
	int tx=0,ty=0;
	//0-255
	if(abs(vx-493)>eps)
	{
		tx=abs(493-vx);
		if(vx>493)
		{
			tx=tx*1.0/531*255;
			tx*=Alpha;
			analogWrite(R,tx);
			analogWrite(L,0);
			tx=-tx;
		}
		else
		{
			tx=tx*1.0/493*255;
			tx*=Alpha;
			analogWrite(R,0);
			analogWrite(L,tx);
		}
	}
	else
	{
		analogWrite(R,0);
		analogWrite(L,0);
	}

	if(abs(vy-518)>eps)
	{
		ty=abs(518-vy);
		if(vy>518)
		{
			ty=ty*1.0/506*255;
			ty*=Alpha;
			analogWrite(U,ty);
			analogWrite(D,0);
			ty=-ty;
		}
		else
		{
			ty=ty*1.0/518*255;
			ty*=Alpha;
			analogWrite(U,0);
			analogWrite(D,ty);
		}
	}
	else
	{
		analogWrite(U,0);
		analogWrite(D,0);
	}

	Serial.print(ty);
	Serial.print(" ");
	Serial.print(tx);
	Serial.print("\n");
	delay(100);

}
