#include "rpc.h"
#include "ArduinoJson.h"

typedef enum {
	SetBlinkDelay = 1,
	// Add functions here
} functions;

void clearParamsForResponse(StaticJsonDocument<200>& receiveResponseDoc)
{
	receiveResponseDoc.remove("p");
	receiveResponseDoc["p"] = receiveResponseDoc["p"].to<JsonArray>();
}

void rpc_executeFunction(StaticJsonDocument<200>& receiveResponseDoc)
{
	int funcId = receiveResponseDoc["f"];
	int numParam = receiveResponseDoc["p"].size();

	switch(funcId)
	{
		case SetBlinkDelay:
		{
			extern uint16_t blinkDelay;
			blinkDelay = receiveResponseDoc["p"][0];

			// creating response
      clearParamsForResponse(receiveResponseDoc);
			receiveResponseDoc["p"][0] = 5;
			break;
		}

		default:
		{
			receiveResponseDoc["err"] = "func unknown";
			break;
		}
	}


}
