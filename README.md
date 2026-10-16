# 实验2 串口通信实验

> 平台：STM32F103C8T6 最小系统核心板（Blue Pill）+ CH340 USB/TTL 串口模块
> 环境：STM32CubeMX 6.16.1 + Keil MDK 5 + ST-Link V2 + 串口助手（XCOM / 纸飞机调试助手）

## 实验内容

| 部分 | 内容 |
|---|---|
| 基础1 | 串口协议与 RS-232 / RS-485 标准、TTL 电平区别、CH340 模块工作原理 |
| 基础2 | 两台电脑经 CH340 模块互传文件，验证"文件大小—波特率—传输时间"关系与共地的必要性 |
| 任务一 | USART1 配置为 115200-8-N-1，轮询方式连续发送 `hello windows!`，并实现 `#` 暂停 / `*` 恢复 |
| 任务二 | (1) 串口中断方式重做任务一(2)；(2) USART1_TX → DMA1 通道 4 连续发送 |
| 任务三 | Keil 软件仿真 + 逻辑分析仪观察串口波形，分析时序并计算实际波特率 |

## 目录结构

```
实验2-串口通信实验.md          实验报告（Markdown）
实验2-串口通信实验-博客版.md    博客文稿（配 csdn_images/ 使用）
images/                      报告插图（33 张，含 3 张动图）
csdn_images/                 博客配图（按序号重命名，含对应表）
code/task1/                  任务一：CubeMX 配置 + 轮询收发
code/task2-1/                任务二(1)：接收中断 + 中断发送
code/task2-2/                任务二(2)：USART1_TX → DMA1 通道 4
output/                      报告 PDF、代码 zip、交付说明
```

## 编译与运行

1. 用 Keil MDK 打开 `code/<工程>/MDK-ARM/*.uvprojx`；
2. Rebuild 后把 Debug 选为 **ST-Link Debugger**，下载到开发板；
3. 与上位机连接：模块 **TXD → PA10(USART1_RX)**、**RXD → PA9(USART1_TX)**、**GND → GND**，VCC 不接；
4. 串口助手设为 115200-8-N-1。

任务三使用软件仿真：Options for Target → Debug → **Use Simulator**，Dialog DLL = `DARMSTM.DLL`，Parameter = `-pSTM32F103C8`；进入调试后用 View → Analysis Windows → Logic Analyzer 添加 `USART1_SR`(TXE) 与 `USART1_DR` 两个信号。

## 主要结论

- 不加延时连续发送时**不会丢数据**（轮询发送速率被波特率限制在约 11.5 KB/s），只是串口助手刷屏很快；加 `HAL_Delay(200)` 后可逐行清楚观察。
- 两机传文件：`STM32F4总线架构图.png`（250 224 字节）在 115200 bps 下理论 21.72 s、实测 22 s，偏差仅 +1.3%。
- 任务三：TXE 脉冲间隔实测平均 87.79 µs（比理论值多约 1 µs，来自中断响应开销），USART1 的 BRR = 0x271（USARTDIV = 39.0625）→ 实际波特率 **115 200 bps，误差 0%**。

## 相关链接

- 博客（CSDN）：[实验2 串口通信实验](https://blog.csdn.net/2401_89763261/article/details/168143455)
