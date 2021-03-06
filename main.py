import pandas

from tkinter.filedialog import askopenfilename
from openpyxl.utils import get_column_letter, column_index_from_string

from module import readdata
from module import buildtable
from module import writedata
from header import id2indextable_header


def main():
	# 创建普通报文对象
	msgRoute = readdata.MsgRoute()
	msgRoute.get_file_pathname()
	msgRoute.read_data("O")

	# 创建信号报文对象
	signalRoute = readdata.SignalRoute()
	signalRoute.get_file_pathname()
	signalRoute.read_data("T")

	# 创建写文件对象
	writeData = writedata.WriteData()

	# 创建一个读hex对象
	readHex = readdata.ReadHex()
	readHex.get_file_pathname()
	readHex.read_hex()

	# # 中断MO初始化表
	canFullIdNameISR = buildtable.CanFullIdNameISR()
	canFullIdNameISR.get_valid_data(msgRoute, signalRoute)
	canFullIdNameISR.data_handle()
	canFullIdNameISR.build_table()
	canFullIdNameISR.build_table_len_hex_data(len(canFullIdNameISR.CanFullIDNameISRList))
	canFullIdNameISR.modify_hex_data(readHex.hexData, canFullIdNameISR.tableLenAddr, 1, canFullIdNameISR.lenHexDataList)
	canFullIdNameISR.build_hex_data(canFullIdNameISR.CanFullIDNameISRList)
	canFullIdNameISR.modify_hex_data(readHex.hexData, canFullIdNameISR.tableAddr, canFullIdNameISR.structLen*canFullIdNameISR.tableLen, canFullIdNameISR.hexDataList)

	# 中断轮询表
	pbDirectRoutingTable = buildtable.PbDirectRoutingTable()
	pbDirectRoutingTable.get_valid_data(msgRoute, signalRoute)
	pbDirectRoutingTable.data_handle()
	pbDirectRoutingTable.build_table()
	pbDirectRoutingTable.build_table_len_hex_data(len(pbDirectRoutingTable.routerTableISRList))
	pbDirectRoutingTable.modify_hex_data(readHex.hexData, pbDirectRoutingTable.tableLenAddr, 1, pbDirectRoutingTable.lenHexDataList)
	pbDirectRoutingTable.build_hex_data([subList[1:-3] for subList in pbDirectRoutingTable.routerTableISRList])
	pbDirectRoutingTable.modify_hex_data(readHex.hexData, pbDirectRoutingTable.tableAddr, pbDirectRoutingTable.structLen*pbDirectRoutingTable.tableLen, pbDirectRoutingTable.hexDataList)

	# 报文轮询表
	pbMsgRoutingTable = buildtable.PbMsgRoutingTable()
	pbMsgRoutingTable.get_valid_data(msgRoute, signalRoute)
	pbMsgRoutingTable.data_handle()
	pbMsgRoutingTable.build_table()
	pbMsgRoutingTable.build_table_len_hex_data(len(pbMsgRoutingTable.routerTableFIFOList))
	pbMsgRoutingTable.modify_hex_data(readHex.hexData, pbMsgRoutingTable.tableLenAddr, 1, pbMsgRoutingTable.lenHexDataList)
	pbMsgRoutingTable.build_hex_data([subList[1:-3] for subList in pbMsgRoutingTable.routerTableFIFOList])
	pbMsgRoutingTable.modify_hex_data(readHex.hexData, pbMsgRoutingTable.tableAddr, pbMsgRoutingTable.structLen*pbMsgRoutingTable.tableLen, pbMsgRoutingTable.hexDataList)

	# 信号报文接收表
	pbMsgRecvTable = buildtable.PbMsgRecvTable()
	pbMsgRecvTable.get_valid_data(signalRoute)
	pbMsgRecvTable.data_handle()
	pbMsgRecvTable.build_table()
	pbMsgRecvTable.build_table_len_hex_data(len(pbMsgRecvTable.PBMsgRecvTableList))
	pbMsgRecvTable.modify_hex_data(readHex.hexData, pbMsgRecvTable.tableLenAddr, 1, pbMsgRecvTable.lenHexDataList)
	pbMsgRecvTable.build_hex_data(pbMsgRecvTable.PBMsgRecvTableList)
	pbMsgRecvTable.modify_hex_data(readHex.hexData, pbMsgRecvTable.tableAddr, pbMsgRecvTable.structLen*pbMsgRecvTable.tableLen, pbMsgRecvTable.hexDataList)

	# 信号路由表
	pbSignalRoutingTable = buildtable.PbSignalRoutingTable()
	pbSignalRoutingTable.get_valid_data(signalRoute)
	pbSignalRoutingTable.data_handle()
	pbSignalRoutingTable.build_table()
	pbSignalRoutingTable.build_hex_data(pbSignalRoutingTable.PbSignalRoutingTableList)
	pbSignalRoutingTable.modify_hex_data(readHex.hexData, pbSignalRoutingTable.tableAddr, pbSignalRoutingTable.structLen*pbSignalRoutingTable.tableLen, pbSignalRoutingTable.hexDataList)

	# 信号报文发送表
	pbMsgSendTable = buildtable.PbMsgSendTable()
	pbMsgSendTable.get_valid_data(signalRoute)
	pbMsgSendTable.data_handle()
	pbMsgSendTable.build_table()
	pbMsgSendTable.build_hex_data(pbMsgSendTable.PbMsgSendTableList)
	pbMsgSendTable.modify_hex_data(readHex.hexData, pbMsgSendTable.tableAddr, pbMsgSendTable.structLen*pbMsgSendTable.tableLen, pbMsgSendTable.hexDataList)

	# 目标信号对应源信号ID索引
	pbMsgSrcTable = buildtable.PbMsgSrcTable()
	pbMsgSrcTable.get_valid_data(signalRoute)
	pbMsgSrcTable.data_handle()
	pbMsgSrcTable.build_table()

	# 信号报文发送调度表
	pbMsgSendSchedule = buildtable.PbMsgSendSchedule()
	pbMsgSendSchedule.get_valid_data(signalRoute)
	pbMsgSendSchedule.data_handle()
	pbMsgSendSchedule.build_table()
	pbMsgSendSchedule.build_hex_data(pbMsgSendSchedule.PbMsgSendSchedule)
	pbMsgSendSchedule.modify_hex_data(readHex.hexData, pbMsgSendSchedule.tableAddr, pbMsgSendSchedule.structLen*pbMsgSendSchedule.tableLen, pbMsgSendSchedule.hexDataList)

	# 信号初始值
	pbMsgRevInitVal = buildtable.PbMsgRevInitVal()
	pbMsgRevInitVal.get_valid_data(signalRoute)
	pbMsgRevInitVal.data_handle()
	pbMsgRevInitVal.build_table()

	# 信号失效值
	pbMsgRevDefaultVal = buildtable.PbMsgRevDefaultVal()
	pbMsgRevDefaultVal.get_valid_data(signalRoute)
	pbMsgRevDefaultVal.data_handle()
	pbMsgRevDefaultVal.build_table()

	# 报文索引
	id2IndexTable = buildtable.Id2IndexTable()
	id2IndexTable.get_valid_data(msgRoute, signalRoute)
	id2IndexTable.data_handle()
	id2IndexTable.build_table()
	id2IndexTable.build_hex_data([id2IndexTable.id2IndexTableA])
	id2IndexTable.modify_hex_data(readHex.hexData, id2IndexTable.tableAddrA, id2IndexTable.structLen*id2IndexTable.tableLen, id2IndexTable.hexDataList)
	id2IndexTable.build_hex_data([id2IndexTable.id2IndexTableB])
	id2IndexTable.modify_hex_data(readHex.hexData, id2IndexTable.tableAddrB, id2IndexTable.structLen*id2IndexTable.tableLen, id2IndexTable.hexDataList)
	id2IndexTable.build_hex_data([id2IndexTable.id2IndexTableC])
	id2IndexTable.modify_hex_data(readHex.hexData, id2IndexTable.tableAddrC, id2IndexTable.structLen*id2IndexTable.tableLen, id2IndexTable.hexDataList)
	id2IndexTable.build_hex_data([id2IndexTable.id2IndexTableD])
	id2IndexTable.modify_hex_data(readHex.hexData, id2IndexTable.tableAddrD, id2IndexTable.structLen*id2IndexTable.tableLen, id2IndexTable.hexDataList)
	id2IndexTable.build_hex_data([id2IndexTable.id2IndexTableE])
	id2IndexTable.modify_hex_data(readHex.hexData, id2IndexTable.tableAddrE, id2IndexTable.structLen*id2IndexTable.tableLen, id2IndexTable.hexDataList)
	id2IndexTable.build_hex_data([id2IndexTable.id2IndexTableF])
	id2IndexTable.modify_hex_data(readHex.hexData, id2IndexTable.tableAddrF, id2IndexTable.structLen*id2IndexTable.tableLen, id2IndexTable.hexDataList)
	

	# 写入Table.c文件
	writeData.write_table_c(canFullIdNameISR.CAN_FULL_ID_NAME_ISR)
	writeData.write_table_c(pbDirectRoutingTable.PB_DirectRoutingTable)
	writeData.write_table_c(pbMsgRoutingTable.PB_MsgRoutingTable)
	writeData.write_table_c(pbMsgRecvTable.PB_Msg_Recv_Table)
	writeData.write_table_c(pbSignalRoutingTable.PB_Signal_Routing_Table)
	writeData.write_table_c(pbMsgSendTable.PB_Msg_Send_Table)
	writeData.write_table_c(pbMsgSrcTable.PB_Msg_Src_Table)
	writeData.write_table_c(pbMsgSendSchedule.PB_Msg_Send_Schedule)
	writeData.write_table_c(id2IndexTable.id2index_table_a)
	writeData.write_table_c(id2IndexTable.id2index_table_b)
	writeData.write_table_c(id2IndexTable.id2index_table_c)
	writeData.write_table_c(id2IndexTable.id2index_table_d)
	writeData.write_table_c(id2IndexTable.id2index_table_e)
	writeData.write_table_c(id2IndexTable.id2index_table_f)
	writeData.write_table_c(pbMsgRevInitVal.PB_MsgRevInitVal)
	writeData.write_table_c(pbMsgRevDefaultVal.PB_MsgRevDefaultVal)
	# writeData.write_table_c(id2IndexTable.id2index_table_a)
	# writeData.write_table_c(id2IndexTable.id2index_table_b)
	# writeData.write_table_c(id2IndexTable.id2index_table_c)
	# writeData.write_table_c(id2IndexTable.id2index_table_d)
	# writeData.write_table_c(id2IndexTable.id2index_table_e)
	# writeData.write_table_c(id2IndexTable.id2index_table_f)

	writeData.write_id2index_table_c(id2indextable_header.id2indextable_headerList, id2IndexTable.id2index_table)
	
	writeData.write_hex(readHex.hexData)
	

	print("------------------END-------------------")

if __name__ == '__main__':
	main()