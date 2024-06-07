/*
 * UpDownCounter.c
 *
 * Created: 1/21/2024 9:01:37 AM
 * Author : CEDP
 */ 
#define F_CPU 1000000
#include <util/delay.h>
#include <avr/io.h>

unsigned char upcount(unsigned char count)
{
	unsigned char result;
	result = (count + 3)%16;
	return result;
}

unsigned char downcount(unsigned char count)
{
	unsigned char result;
	result = (count + 16 - 3)%16;
	return result;
}

int main(void)
{
    /* Replace with your application code */
	unsigned char count = 0;
	DDRA = 0b11111100;
	DDRB = 0b00001111;
	
	unsigned char prev1, prev2;
	prev1 = prev2 = 0;
	
    while (1) 
    {
		unsigned char in;
		in = PINA;
		
		if(in & 0x01)       // first switch at A0
		{
			if(prev1 == 0)
			{
				count = upcount(count);
			}
		}
		if(in & 0x02)  // first switch at A1
		{
			if(prev2 == 0)
			{
				count = downcount(count);
			}
		}
		
		prev1 = in&(0x01);
		prev2 = in&(0x02);
		
		PORTB = count;
		_delay_ms(1000);
    }
}

