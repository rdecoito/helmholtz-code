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
//Clock registers pointers
static volatile unsigned char *CSCTL0_H_;
static volatile unsigned int *CSCTL1_;
static volatile unsigned int *CSCTL2_;
static volatile unsigned int *CSCTL3_;

/*------------------------------------------------------*/
//eUSCI UART registers pointers
static volatile unsigned int *UCA0CTLW0_;
static volatile unsigned int *UCA0CTLW1_;
static volatile unsigned int *UCA0BRW_;
static volatile unsigned int *UCA0MCTLW_;
static volatile unsigned int *UCA0STATW_;
static volatile unsigned int *UCA0RXBUF_;
static volatile unsigned int *UCA0TXBUF_;
static volatile unsigned int *UCA0IE_;
static volatile unsigned int *UCA0IFG_;
static volatile unsigned int *UCA0IV_;

/**
 * Acts as a constructor, assigning the peripheral addresses to the
 * pointers. Must be called first
 */
void UART();

/**
 * Begins initialization of UART configuring the pins for receiving data
 * calling initUART, which initializes the eUSCI UART registers for receiving
 * data based on the given parameters and sets a buffer to use for eUSCI UART.
 */
void beginInit(uint32_t baud, unsigned int srcClk, uint32_t srcClkHz, uint8_t *buffer, size_t buff_size);

/**
 * Initializes eUSCI UART registers for receiving data
 */
static void initUART(uint32_t baud, unsigned int srcClk, uint32_t srcClkHz);

/**
 * Sets MCLK and SMCLK to source the DCO at 1MHz
 */
static void setClk(void);

/**
 * Checks whether eUSCI_A is currently tranmitting/receiving
 * Returns 1 if transmitting/receiving, 0 if not
 */
inline uint8_t isInProgress(void)
{
    return *UCA0STATW_ & UCBUSY;
}

/**
 * Reads a single character from the ring buffer
 */
uint8_t read(void);

/**
 * Reads the entirety of the ring buffer and places its contents into the given
 * buffer
 */
size_t readAndSet(uint8_t *buffer, size_t size);

void endUART(void);

inline size_t available(void)
{
    return size();
}

/**
 * Returns the baudrate
 */
inline uint32_t getBaudrate(void)
{
    return baudrate;
}

inline void clear(void)
{
    empty();
}


__interrupt void USCIA0_ISR();

#endif





