import sys
import time
import traceback

from extract import extract_data
from load import load_data
from transform import drop_col,rename_df





if __name__ == '__main__':
    start_time = time.perf_counter()
    print(f"Started pipeline\n")

    try:
        raw_data = extract_data()
        dropped_cols = drop_col(raw_data)
        clean_data = rename_df(dropped_cols)
        load_data(clean_data)

        pipeline_success = True

    except Exception as e:
        print(f"Pipeline failed due to error: {e}")
        traceback.print_exc()

    finally:
        end_time = time.perf_counter()
        execution_time = end_time - start_time

        if pipeline_success:
            print(f"\nPipeline completed successfully in {execution_time:.6f} seconds\n")
        else:
            print(f"\nPipeline failed after {execution_time:.6f} seconds\n")
            sys.exit(1)



    # 
    # print(f"Started pipeline\n")

    # try:
    #     raw_data = extract_data()
    #     dataframe = drop_col(raw_data)
    #     rename_df(dataframe)
    #     pipeline_success = True
       
    # except Exception as e:
    #     print(f"Pipeline failed due to error: {e}")
    #     traceback.print_exc()
        
    # finally:
    #     end_time = time.perf_counter()
    #     execution_time = end_time - start_time

    #     if pipeline_success:
    #         print(f"\nPipeline completed successfully in {execution_time:.6f} seconds\n")
    #     else:
    #         print(f"\nPipeline failed after {execution_time:.6f} seconds\n")
    #         sys.exit(1)


        
