

#define F_CPU 1000000
#include <avr/io.h>
#include <util/delay.h>
#include <avr/interrupt.h>

// this array will change for different patterns

volatile unsigned char image[8] = 
{ 0b11101111, 0b11100111, 0b11101011, 0b11101111, 0b11101111, 0b10000011, 0b11111111, 0b11111111 };
	
volatile unsigned char column_selector = 0b10000000;
volatile unsigned char toggle = 1;

ISR(INT0_vect){
	toggle = ~toggle;
}

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

int main(void)
{
    DDRA = 0xFF;
    DDRB = 0xFF;
	
	GICR = (1<<INT0);
	MCUCR = MCUCR & 0b00000011;
	sei();
	
    while (1) 
    {
		for(int i=0; i<50; i++){
			show_image();
		}
		
		if((toggle & 0b00000001)){	// if push button pressed, make the image dynamic
			_delay_ms(80);	
			column_selector = get_next_column_selector_down(column_selector);
		}
    }
}
