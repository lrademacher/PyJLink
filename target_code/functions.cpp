// TODO: Maybe provide more abstract interface than directly binson?
#include "rpc.h"
#include "ArduinoJson.h"

void rpc_executeFunction(StaticJsonDocument<200>& receiveDoc)
{
	int funcId = receiveDoc["f"];
	int numParam = receiveDoc["p"].size();

	switch(funcId)
	{
		case 1:
		{
			extern uint16_t blinkDelay;
			blinkDelay = receiveDoc["p"][0];
//			receiveDoc["p"] = doc.to<JsonArray>();
			receiveDoc.remove("p");
			receiveDoc["p"] = receiveDoc["p"].to<JsonArray>();
			receiveDoc["p"][0] = 5;
			break;
		}
	}


}
