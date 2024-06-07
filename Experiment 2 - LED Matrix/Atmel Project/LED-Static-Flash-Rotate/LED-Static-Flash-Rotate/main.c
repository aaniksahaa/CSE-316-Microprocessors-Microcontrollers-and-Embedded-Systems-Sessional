/*
 * LED-Static-Flash-Rotate.c
 *
 * Created: 1/27/2024 8:35:45 PM
 * Author : Anik Saha - 2005001
 */ 

#define F_CPU 1000000
#include <avr/io.h>
#include <util/delay.h>

// this array will change for different patterns

volatile unsigned char image[8]
= { 0b11101111, 0b11100111, 0b11101011, 0b11101111, 0b11101111, 0b10000011, 0b11111111, 0b11111111 };


volatile unsigned char image_rotate[4][8]
= {
	{ 0b11101111, 0b11100111, 0b11101011, 0b11101111, 0b11101111, 0b10000011, 0b11111111, 0b11111111 },
	{ 0b11111111, 0b11111111, 0b11011011, 0b10111011, 0b00000011, 0b11111011, 0b11111011, 0b11111111 },
	{ 0b11111111, 0b11111111, 0b11000001, 0b11110111, 0b11110111, 0b11010111, 0b11100111, 0b11110111 },
	{ 0b11111111, 0b11011111, 0b11011111, 0b11000000, 0b11011101, 0b11011011, 0b11111111, 0b11111111 }
};



volatile unsigned char blankscreen[8] =
{ 0b11111111, 0b11111111, 0b11111111, 0b11111111, 0b11111111, 0b11111111, 0b11111111, 0b11111111 };

volatile unsigned char column_selector = 0b10000000;

unsigned char get_next_column_selector_down(unsigned char current_column_selector){
	unsigned char next_column_selector;
	
	// moving down
	next_column_selector = current_column_selector >> 1;
	if( ! next_column_selector ){
		next_column_selector = 0b10000000;
	}
	
	return next_column_selector;
}

unsigned char get_next_column_selector_up(unsigned char current_column_selector){
	unsigned char next_column_selector;
	
	// moving down
	next_column_selector = current_column_selector << 1;
	if( ! next_column_selector ){
		next_column_selector = 0b00000001;
	}
	
	return next_column_selector;
}

void show_image(){
	PORTA = column_selector;
	for (int i=0; i<8; i++){
		PORTB = image[i];
		_delay_ms(.5);
		unsigned char c = PORTA;
		c = get_next_column_selector_down(c);
		PORTA = c;
	}
}

void show_rotated_image(int phase){
	PORTA = column_selector;
	for (int i=0; i<8; i++){
		PORTB = image_rotate[phase][i];
		_delay_ms(.5);
		unsigned char c = PORTA;
		c = get_next_column_selector_down(c);
		PORTA = c;
	}
}

void show_blankscreen(){
	PORTA = column_selector;
	for (int i=0; i<8; i++){
		PORTB = blankscreen[i];
		_delay_ms(.5);
		unsigned char c = PORTA;
		c = get_next_column_selector_down(c);
		PORTA = c;
	}
}

void show_static(){
	for(int i=0; i<50; i++){
		show_image();
	}
}

void show_flash(){
	for(int i=0; i<100; i++){
		show_image();
	}
	for(int i=0; i<100; i++){
		show_blankscreen();
	}
}

void show_rotation(){
	for(int i=0; i<3; i++)
	{
		for(int j=0; j<200; j++)
		{
			show_rotated_image(i);	
		}
	}
}

int main(void)
{
	DDRA = 0xFF;
	DDRB = 0xFF;
	
	while (1)
	{
		//show_static();
		//show_flash();
		show_rotation();
	}
}


