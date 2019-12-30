#ifndef UART_H
#define UART_H
#include <msp430.h>
#include <stdint.h>
#include "RingBuffer.h"

static uint32_t baudrate = 0;
static unsigned int UCA0BRW_Val = 0;
static unsigned char UCABRF_Val = 0;
static int16_t UCBRS_mask = 0;
static double lookup = 0;

/*------------------------------------------------------*/
//Clock registers
volatile unsigned char *CSCTL0_H_ = CSCTL0_H;
volatile unsigned int *CSCTL1_ = CSCTL1;
volatile unsigned int *CSCTL2_ = CSCTL2;
volatile unsigned int *CSCTL3_ = CSCTL3;

/*------------------------------------------------------*/
//eUSCI UART registers
volatile unsigned int *UCA0CTLW0_ = (volatile unsigned int *) &UCA0CTLW0;
volatile unsigned int *UCA0CTLW1_ = (volatile unsigned int *) &UCA0CTLW1;
volatile unsigned int *UCA0BRW_ = (volatile unsigned int *) &UCA0BRW;
volatile unsigned int *UCA0MCTLW_ = (volatile unsigned int *) &UCA0MCTLW;
volatile unsigned int *UCA0STATW_ = (volatile unsigned int *) &UCA0STATW;
volatile unsigned int *UCA0RXBUF_ = (volatile unsigned int *) &UCA0RXBUF;
volatile unsigned int *UCA0TXBUF_ = (volatile unsigned int *) &UCA0TXBUF;
volatile unsigned int *UCA0IE_ = (volatile unsigned int *) &UCA0IE;
volatile unsigned int *UCA0IFG_ = (volatile unsigned int *) &UCA0IFG;
volatile unsigned int *UCA0IV_ = (volatile unsigned int *) &UCA0IV;

/*Begins initialization of UART configuring the pins for receiving data
 * calling initUART, which initializes the eUSCI UART registers for receiving
 * data based on the given parameters and sets a buffer to use for eUSCI UART.
 */
void beginInit(uint32_t baud, unsigned int srcClk, uint32_t srcClkHz, uint8_t *buffer, size_t buff_size);

/*Initializes eUSCI UART registers for receiving data
 */
static void initUART(uint32_t baud, unsigned int srcClk, uint32_t srcClkHz);

/*Sets MCLK and SMCLK to source the DCO at 1MHz
 */
static void setClk(void);

/*Checks whether eUSCI_A is currently tranmitting/receiving
 * Returns 1 if transmitting/receiving, 0 if not
 */
inline uint8_t isInProgress(void)
{
    return *UCA0STATW_ & UCBUSY;
}

/*Reads a single character from the ring buffer
 */
uint8_t read(void);

/*Reads the entirety of the ring buffer and places its contents into the given
 * buffer
 */
size_t readAndSet(uint8_t *buffer, size_t size);

void endUART(void);

inline size_t available(void)
{
    size();
}

/*Returns the baudrate
 */
inline uint32_t getBaudrate(void)
{
    return baudrate;
}

inline void clear(void)
{
    reset();
}

#endif





