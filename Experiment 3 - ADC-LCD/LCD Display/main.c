#ifndef F_CPU
#define F_CPU 1000000UL // 16 MHz clock speed
#endif
#define D4 eS_PORTD4
#define D5 eS_PORTD5
#define D6 eS_PORTD6
#define D7 eS_PORTD7
#define RS eS_PORTC6
#define EN eS_PORTC7

#include <avr/io.h>
#include <util/delay.h>
#include <stdio.h>
#include "lcd.h" //Can be download from the bottom of this article

void ADC_init() {
	ADMUX |= (1 << REFS0);
	ADCSRA |= (1 << ADEN) | (1 << ADPS2) | (1 << ADPS1) | (1 << ADPS0);
}

uint16_t ADC_read(uint8_t channel) {
	ADMUX = (ADMUX & 0xF0) | (channel & 0x0F);
	ADCSRA |= (1 << ADSC);
	while (ADCSRA & (1 << ADSC));
	return ADC;
}

void printVoltageToLcd(float voltage){
	char s[16];
	int intPortion = (int)voltage;
	sprintf(s, "%d", intPortion);
	Lcd4_Write_String(s);
	
	Lcd4_Write_Char('.');
	
	int decimalPortion = ((int)(voltage * 100)) % 100;
	sprintf(s, "%d", decimalPortion);
	Lcd4_Write_String(s);
}

int main(void)
{
	DDRD = 0xFF;
	DDRC = 0xFF;
	// int i;
	ADC_init();
	Lcd4_Init();
	uint16_t adc_value;
	float voltage;
	while(1)
	{
		adc_value = ADC_read(0);
		voltage = (float)adc_value * 5.0 / 1024.0;
		//sprintf(s, "%0.2f V", 12.5);
		Lcd4_Set_Cursor(1,1);
		//Lcd4_Write_String(s);
		printVoltageToLcd(voltage);
		
		
		/*
		Lcd4_Set_Cursor(1,1);
		Lcd4_Write_String("electroSome LCD Hello World");
		for(i=0;i<15;i++)
		{
			_delay_ms(500);
			Lcd4_Shift_Left();
		}
		for(i=0;i<15;i++)
		{
			_delay_ms(500);
			Lcd4_Shift_Right();
		}
		Lcd4_Clear();
		Lcd4_Set_Cursor(2,1);
		Lcd4_Write_Char('e');
		Lcd4_Write_Char('S');
		_delay_ms(2000);
		*/
	}
}