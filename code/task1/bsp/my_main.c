#include "my_main.h"

/* 发送缓冲区 */
char uart_tx_data[30];

/* 初始化函数：本步只做发送，暂时没有需要初始化的内容 */
void setup(void)
{

}

/* 主循环：轮询（阻塞）方式连续发送 hello windows!
 * HAL_UART_Transmit 内部逐字节等待 TXE 标志，一帧发完之前 CPU 一直停在该函数里；
 * 这里故意不加任何延时，用于观察上位机（串口助手）是否出现接收数据丢失。 */
void loop(void)
{
	sprintf(uart_tx_data,"hello windows!\r\n");
	HAL_UART_Transmit(&huart1,(uint8_t *)uart_tx_data,strlen(uart_tx_data),30);
}
