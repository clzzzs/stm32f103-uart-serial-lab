#include "my_main.h"

char uart_tx_data[30];
uint8_t rx_byte;
uint8_t uart_flag = 1;

void setup(void)
{
	HAL_UART_Receive_IT(&huart1, &rx_byte, 1);
}

void loop(void)
{
	if(uart_flag == 1)
	{
		sprintf(uart_tx_data,"hello windows!\r\n");
		HAL_UART_Transmit_IT(&huart1,(uint8_t *)uart_tx_data,(uint16_t)strlen(uart_tx_data));
		HAL_Delay(200);
	}
}

void HAL_UART_RxCpltCallback(UART_HandleTypeDef *huart)
{
	if(huart->Instance == USART1)
	{
		if(rx_byte == '#')
			uart_flag = 0;
		else if(rx_byte == '*')
			uart_flag = 1;

		HAL_UART_Receive_IT(&huart1, &rx_byte, 1);
	}
}
