#include <cstdlib>
#include <DynamixelWorkbench.h>

void Model_Scan(uint8_t* scanned_id, const char* port_name, int baud_rate);

DynamixelWorkbench dxl_wb;

int main(int argc, char *argv[]) 
{
    const char* port_name = "/dev/ttyUSB0";
    int baud_rate = 1000000;

    (void)argc; (void)argv;

    uint8_t scanned_id[16];
    Model_Scan(scanned_id, port_name, baud_rate);

    return 0;
}

void Model_Scan(uint8_t* scanned_id, const char* port_name, int baud_rate)
{
    const char *log;
    bool result = false;
    uint8_t dxl_cnt = 0;
    uint8_t range = 100;

    result = dxl_wb.init(port_name, baud_rate, &log);

    if (!result)
    {
        printf("%s\n", log);
        printf("Failed to init\n");
        return;
    }
    else
    {
        printf("Succeeded to init(%d)\n", baud_rate);  
    }

    printf("Wait for scan...\n");
    result = dxl_wb.scan(scanned_id, &dxl_cnt, range, &log);
    if (!result)
    {
        printf("%s\n", log);
        printf("Failed to scan\n");
    }
    else
    {
        printf("Find %d Dynamixels\n", dxl_cnt);
    }

    for (int cnt = 0; cnt < dxl_cnt; cnt++)
    {
        uint16_t model_number = 0;
        result = dxl_wb.ping(scanned_id[cnt], &model_number, &log);
        printf("id : %d, model name : %s, model_number : %d\n", scanned_id[cnt], dxl_wb.getModelName(scanned_id[cnt]), model_number);
    }
        
    return;
}
