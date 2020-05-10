#include "rpc.h"
#include "SEGGER_RTT.h"
#include "ArduinoJson.h"

uint32_t receiveIdx = 0;
char receiveBuf[200];
StaticJsonDocument<200> receiveDoc;
char transmitBuf[200];

#define RTT_BUF 0

void rpc_executeFunction(StaticJsonDocument<200>& receiveDoc);

extern "C" void rpc_process() {
	unsigned bytesRead = SEGGER_RTT_Read(RTT_BUF, &receiveBuf[receiveIdx], sizeof(receiveBuf) - receiveIdx);
	receiveIdx += bytesRead;
	char* delim_ptr = (char*) memchr (receiveBuf, '\0', receiveIdx);
	if(delim_ptr)
	{
		DeserializationError error = deserializeJson(receiveDoc, receiveBuf);
		if(!error)
		{
			rpc_executeFunction(receiveDoc);
		}

		int bytesToDelim = delim_ptr-receiveBuf+1;
		if(receiveIdx > bytesToDelim)
		{
			memcpy(receiveBuf, delim_ptr + 1, receiveIdx - bytesToDelim);
		}

		receiveIdx -= bytesToDelim;

		size_t responseSize = serializeJson(receiveDoc, transmitBuf);

		SEGGER_RTT_Write(RTT_BUF, transmitBuf, responseSize);
	}
}

void rpc_response() {

}
