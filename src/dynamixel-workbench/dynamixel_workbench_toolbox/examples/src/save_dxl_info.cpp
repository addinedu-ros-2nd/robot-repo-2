#include <DynamixelWorkbench.h>
#include <cstdlib>
#include <dynamixel_item.h>

bool Initialize_DXL(uint8_t *scanned_id, const char *port_name, int baud_rate);
int32_t Read_Present_Position(uint8_t dxl_id);
bool MinMax_Position_Setting(uint8_t *scanned_id);
void Set_PID_Param(uint8_t *scanned_id);
void Print_DXL_Setting(uint8_t *scanned_id);
void Print_DXL_Info(uint8_t *scanned_id, int i);

DynamixelWorkbench dxl_wb;

int main(int argc, char *argv[]) {
  (void)argc; // No using argc
  (void)argv; // No using argv

  // Liux defalut USB port
  const char *port_name = "/dev/ttyUSB0";
  // Open_Manipulator defalut baud_rate
  int baud_rate = 1000000;

  // Get Dynamixel id array and initialize DXL
  uint8_t scanned_id[5];
  if (!Initialize_DXL(scanned_id, port_name, baud_rate))
  {
    printf("Fail to initialize");
    return 0;
  }

  // Check DXL setting
  Print_DXL_Setting(scanned_id);

  bool tmp = 1;
  while(true){
    if (tmp)
    {
      tmp = 0;
      dxl_wb.goalPosition(scanned_id[0], (int32_t) 4000);
    }
    else
    {
      tmp = 1;
      dxl_wb.goalPosition(scanned_id[0], (int32_t) 3500);
    }
    for (int j=0;j<6;j++){
      int i=0;
      Print_DXL_Info(scanned_id, i);
      sleep(1);
    }
  }

  // while(true){
  //     sleep(1);
  //     int32_t data = 0;
  //     printf("Present_Position:");
  //     for (int i=0;i<5;i++){
  //         dxl_wb.readRegister(scanned_id[i], "Present_Position", &data);
  //         printf(" %d", data);
  //     }
  //     printf("\n");
  // }
  
  // for (int i=0;i<5;i++){
  //     printf("\n\n\n\n\n\n\n\n\n\n\n");
  //     printf("rpm:                           %f\n", dxl_wb.getModelInfo(scanned_id[i])[0].rpm);
  //     printf("value_of_min_radian_position:  %ld\n", dxl_wb.getModelInfo(scanned_id[i])[0].value_of_min_radian_position);
  //     printf("value_of_zero_radian_position: %ld\n", dxl_wb.getModelInfo(scanned_id[i])[0].value_of_zero_radian_position);
  //     printf("value_of_max_radian_position:  %ld\n", dxl_wb.getModelInfo(scanned_id[i])[0].value_of_max_radian_position);
  //     printf("min_radian:                    %f\n", dxl_wb.getModelInfo(scanned_id[i])[0].min_radian);
  //     printf("max_radian:                    %f\n", dxl_wb.getModelInfo(scanned_id[i])[0].max_radian);
  // }

  // for (int i=0;i<1;i++){
  //     printf("%d\n", dxl_wb.getTheNumberOfControlItem(scanned_id[i]));
  //     const ControlItem *item = dxl_wb.getControlTable(scanned_id[i]);
  //     for (int j=0; j<dxl_wb.getTheNumberOfControlItem(scanned_id[i]); j++){
  //         printf("id:%d==========================\n", scanned_id[i]);
  //         printf("item_name:        %s\n", item[j].item_name);
  //         printf("address:          %d\n", item[j].address);
  //         printf("item_name_length: %d\n", item[j].item_name_length);
  //         printf("data_length:      %d\n", item[j].data_length);
  //     }
  // }

  return 0;
}

bool Initialize_DXL(uint8_t *scanned_id, const char *port_name, int baud_rate) {
  const char *log;
  bool result = false;
  uint8_t dxl_cnt = 0;
  uint8_t range = 100;

  // Initialize
  result = dxl_wb.init(port_name, baud_rate, &log);
  if (!result) {
    printf("%s\n", log);
    printf("Failed to init");
    return result;
  }
 
  // Find models
  result = dxl_wb.scan(scanned_id, &dxl_cnt, range, &log);
  if (!result) {
    printf("%s\n", log);
    printf("Failed to scan");
    return result;
  }

  // Initial setting
  // MinMax_Position_Setting(scanned_id);

  // Print model info
  for (int i = 0; i < dxl_cnt; i++) {
    // ping
    uint16_t model_number = 0;
    result = dxl_wb.ping(scanned_id[i], &model_number, &log);
    if (!result) {
      printf("%s\n", log);
      printf("Failed to ping");
      return result;
    }

    // Set joint mode
    result = dxl_wb.jointMode(scanned_id[i], 10, 10, &log);
    if (!result) {
      printf("%s\n", log);
      printf("Failed to set jointMode");
      return result;
    }
    printf("id : %d, model name : %s, model_number : %d\n", scanned_id[i],
           dxl_wb.getModelName(scanned_id[i]), model_number);
  }

  // PID parameter setting
  Set_PID_Param(scanned_id);

  return result;
}

int32_t Read_Present_Position(uint8_t dxl_id) {
  const char *log;
  bool result = false;
  int32_t get_data = 0;

  result = dxl_wb.itemRead(dxl_id, "Present_Position", &get_data, &log);
  if (!result) {
    printf("%s\n", log);
    printf("Failed to get present position\n");
    return -1;
  } else {
    printf("id:%d, position : %d\n", dxl_id, get_data);
  }

  return get_data;
}

bool MinMax_Position_Setting(uint8_t *scanned_id){
  bool result = false;
  result = dxl_wb.writeRegister(scanned_id[0],
                                "Min_Position_Limit", 0);
  result = dxl_wb.writeRegister(scanned_id[0],
                                "Max_Position_Limit", 4095);
  result = dxl_wb.writeRegister(scanned_id[1],
                                "Min_Position_Limit", 0);
  result = dxl_wb.writeRegister(scanned_id[1],
                                "Max_Position_Limit", 4095);
  result = dxl_wb.writeRegister(scanned_id[2],
                                "Min_Position_Limit", 0);
  result = dxl_wb.writeRegister(scanned_id[2],
                                "Max_Position_Limit", 4095);
  result = dxl_wb.writeRegister(scanned_id[3],
                                "Min_Position_Limit", 0);
  result = dxl_wb.writeRegister(scanned_id[3],
                                "Max_Position_Limit", 4095);
  result = dxl_wb.writeRegister(scanned_id[4],
                                "Min_Position_Limit", 0);
  result = dxl_wb.writeRegister(scanned_id[4],
                                "Max_Position_Limit", 4095);
  return result;
}

void Set_PID_Param(uint8_t *scanned_id){
  bool result = true;
  int32_t DGain = 500;
  int32_t IGain = 0;
  int32_t PGain = 70;
  int32_t F2Gain = 1000;
  int32_t F1Gain = 100;
  result = dxl_wb.writeRegister(scanned_id[0],
                                "Position_D_Gain", DGain);
  result = dxl_wb.writeRegister(scanned_id[0],
                                "Position_I_Gain", IGain);
  result = dxl_wb.writeRegister(scanned_id[0],
                                "Position_P_Gain", PGain);
  result = dxl_wb.writeRegister(scanned_id[0],
                                "Feedforward_2nd_Gain", F2Gain);
  result = dxl_wb.writeRegister(scanned_id[0],
                                "Feedforward_1nd_Gain", F1Gain);
                                
  result = dxl_wb.writeRegister(scanned_id[1],
                                "Position_D_Gain", DGain);
  result = dxl_wb.writeRegister(scanned_id[1],
                                "Position_I_Gain", IGain);
  result = dxl_wb.writeRegister(scanned_id[1],
                                "Position_P_Gain", PGain);
  result = dxl_wb.writeRegister(scanned_id[1],
                                "Feedforward_2nd_Gain", F2Gain);
  result = dxl_wb.writeRegister(scanned_id[1],
                                "Feedforward_1nd_Gain", F1Gain);
                                
  result = dxl_wb.writeRegister(scanned_id[2],
                                "Position_D_Gain", DGain);
  result = dxl_wb.writeRegister(scanned_id[2],
                                "Position_I_Gain", IGain);
  result = dxl_wb.writeRegister(scanned_id[2],
                                "Position_P_Gain", PGain);
  result = dxl_wb.writeRegister(scanned_id[2],
                                "Feedforward_2nd_Gain", F2Gain);
  result = dxl_wb.writeRegister(scanned_id[2],
                                "Feedforward_1nd_Gain", F1Gain);
                                
  result = dxl_wb.writeRegister(scanned_id[3],
                                "Position_D_Gain", DGain);
  result = dxl_wb.writeRegister(scanned_id[3],
                                "Position_I_Gain", IGain);
  result = dxl_wb.writeRegister(scanned_id[3],
                                "Position_P_Gain", PGain);
  result = dxl_wb.writeRegister(scanned_id[3],
                                "Feedforward_2nd_Gain", F2Gain);
  result = dxl_wb.writeRegister(scanned_id[3],
                                "Feedforward_1nd_Gain", F1Gain);
                                
  result = dxl_wb.writeRegister(scanned_id[4],
                                "Position_D_Gain", DGain);
  result = dxl_wb.writeRegister(scanned_id[4],
                                "Position_I_Gain", IGain);
  result = dxl_wb.writeRegister(scanned_id[4],
                                "Position_P_Gain", PGain);
  result = dxl_wb.writeRegister(scanned_id[4],
                                "Feedforward_2nd_Gain", F2Gain);
  result = dxl_wb.writeRegister(scanned_id[4],
                                "Feedforward_1nd_Gain", F1Gain);

  return;
}

void Print_DXL_Setting(uint8_t *scanned_id){
  for (int i=0;i<5;i++){
      int32_t data = 0;
      printf("\nid:%d=======================\n", scanned_id[i]);
      dxl_wb.readRegister(scanned_id[i], "Position_D_Gain", &data);
      printf("Position_D_Gain: %d\n", data);
      dxl_wb.readRegister(scanned_id[i], "Position_I_Gain", &data);
      printf("Position_I_Gain: %d\n", data);
      dxl_wb.readRegister(scanned_id[i], "Position_P_Gain", &data);
      printf("Position_P_Gain: %d\n", data);
      dxl_wb.readRegister(scanned_id[i], "Feedforward_2nd_Gain", &data);
      printf("Feedforward_2nd_Gain: %d\n", data);
      dxl_wb.readRegister(scanned_id[i], "Feedforward_1nd_Gain", &data);
      printf("Feedforward_1nd_Gain: %d\n", data);
      dxl_wb.readRegister(scanned_id[i], "Max_Position_Limit", &data);
      printf("Max_Position_Limit: %d\n", data);
      dxl_wb.readRegister(scanned_id[i], "Min_Position_Limit", &data);
      printf("Min_Position_Limit: %d\n", data);
  }
}

void Print_DXL_Info(uint8_t *scanned_id, int i){
  int32_t data = 0;
  printf("\nid:%d=================================\n", scanned_id[i]);
  dxl_wb.readRegister(scanned_id[i], "Moving_Status", &data);
  printf("Moving_Status: %d\n", data);
  dxl_wb.readRegister(scanned_id[i], "Hardware_Error_Status", &data);
  printf("Hardware_Error_Status: %d\n", data);
  // dxl_wb.readRegister(scanned_id[i], "Goal_PWM", &data);
  // printf("Goal_PWM: %d\n", data);
  // dxl_wb.readRegister(scanned_id[i], "Goal_Current", &data);
  // printf("Goal_Current: %d\n", data);
  // dxl_wb.readRegister(scanned_id[i], "Goal_Velocity", &data);
  // printf("Goal_Velocity: %d\n", data);
  // dxl_wb.readRegister(scanned_id[i], "Goal_Position", &data);
  // printf("Goal_Position: %d\n", data);
  dxl_wb.readRegister(scanned_id[i], "Present_PWM", &data);
  printf("Present_PWM: %d\n", data);
  dxl_wb.readRegister(scanned_id[i], "Present_Current", &data);
  printf("Present_Current: %d\n", data);
  dxl_wb.readRegister(scanned_id[i], "Present_Velocity", &data);
  printf("Present_Velocity: %d\n", data);
  dxl_wb.readRegister(scanned_id[i], "Present_Position", &data);
  printf("Present_Position: %d\n", data);
  // dxl_wb.readRegister(scanned_id[i], "Present_Input_Voltage", &data);
  // printf("Present_Input_Voltage: %d\n", data);
  // dxl_wb.readRegister(scanned_id[i], "Present_Temperature", &data);
  // printf("Present_Temperature: %d\n", data);
  dxl_wb.readRegister(scanned_id[i], "Position_D_Gain", &data);
  printf("Position_D_Gain: %d\n", data);
  dxl_wb.readRegister(scanned_id[i], "Position_I_Gain", &data);
  printf("Position_I_Gain: %d\n", data);
  dxl_wb.readRegister(scanned_id[i], "Position_P_Gain", &data);
  printf("Position_P_Gain: %d\n", data);
  dxl_wb.readRegister(scanned_id[i], "Feedforward_2nd_Gain", &data);
  printf("Feedforward_2nd_Gain: %d\n", data);
  dxl_wb.readRegister(scanned_id[i], "Feedforward_1nd_Gain", &data);
  printf("Feedforward_1nd_Gain: %d\n", data);
}


