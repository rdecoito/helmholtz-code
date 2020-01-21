/*
 * RingBuffer.c
 *
 *  Created on: Dec 28, 2019
 *      Author: Matthew Middleton
 */

#include "../inc/RingBuffer.h"

void initRingBuff(uint8_t *buffer, size_t size)
{
    ring_buffer = buffer;
    max_size = size;
}

uint8_t get(void)
{
    uint8_t val = ring_buffer[tail];

    full = 0;
    tail = (tail+1) % max_size;

    return val;
}

void empty()
{
    head = tail;
    full = 0;
}









