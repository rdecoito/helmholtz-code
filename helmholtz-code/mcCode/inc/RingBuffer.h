/*
 * RingBuffer.h
 *
 *  Created on: Dec 28, 2019
 *      Author: Matthew Middleton
 */

#ifndef RINGBUFFER_H_
#define RINGBUFFER_H_
#include <stdlib.h>
#include <stdint.h>

static size_t head = 0;
static size_t tail = 0;
static size_t max_size;
static uint8_t *ring_buffer = NULL;
static uint8_t full = 0;

/**
 * Initializes the ring buffer by assigning the given buffer to the internal
 * ring buffer and setting the max size that the buffer can hold
 */
void initRingBuff(uint8_t *buffer, size_t size);

/**
 * Places the given data into the ring buffer
 */
inline void put(uint8_t data)
{
    ring_buffer[head] = data;

        if(full)
        {
            tail = (tail+1) % max_size;
        }

        head = (head+1) % max_size;

        full = head==tail;
}

/**
 * Retrieves the data from the ring buffer
 */
uint8_t get(void);

/**
 * Sets the buffer to a state where it may be considered empty
 * and the head and tail are the same
 */
void empty();

/**
 * Determines if the buffer is empty
 * Returns a non-zero, positive integer if empty, 0 if emtpy
 */
inline uint8_t isEmpty(void)
{
    //if head and tail are equal, we are empty
    return (!full && (head==tail));
}

/*Determines if the buffer is full
 * Returns non-zero, positive integer if full, 0 if empty
 */
inline uint8_t isFull(void)
{
    //If tail is ahead the head by 1, we are full
    return full;
}

/*Returns the maximum size that the ring buffer can hold
 */
inline size_t capacity(void)
{
    return max_size;
}

/*Determines how much space is left in the ring buffer
 */
inline size_t size(void)
{
    size_t size = max_size;

    if(!full)
    {
        if(head>=tail)
        {
            size = head-tail;
        }
        else
        {
            size = max_size + head - tail;
        }
    }

    return size;
}

#endif








