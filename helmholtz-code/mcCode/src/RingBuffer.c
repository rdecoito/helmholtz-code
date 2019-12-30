/*
 * RingBuffer.c
 *
 *  Created on: Dec 28, 2019
 *      Author: Matthew Middleton
 */

#include "RingBuffer.h"

void initRingBuff(uint8_t *buffer, size_t size)
{
    ring_buffer = buffer;
    max_size = size;
}

void put(uint8_t data)
{
    (*ring_buffer)[head] = data;

    if(full)
    {
        tail = (tail+1) % max_size;
    }

    head = (head+1) % max_size;

    full = head==tail;
}

uint8_t get(void)
{
    uint8_t val = (*ring_buffer)[tail];

    full = 0;
    tail = (tail+1) % max_size;

    return val;
}

void reset()
{
    head = tail;
    full = 0;
}









