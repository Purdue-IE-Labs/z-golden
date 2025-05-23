import zenoh

with zenoh.open(zenoh.Config()) as session:
    test_t_1 = session.new_timestamp()
    test_t_2 = session.new_timestamp()
    test_s_1 = test_t_1.to_string_rfc3339_lossy()
    test_s_2 = test_t_2.to_string_rfc3339_lossy()
    test_ts_1 = test_t_1.parse_rfc3339(test_s_1) 
    test_ts_2 = test_t_2.parse_rfc3339(test_s_2) 
    yeet = test_t_1 == test_ts_1 


    get_time1 = test_t_1.get_time()
    test_str = str(test_t_1).split("/")[0]
    test_uuid = str(test_t_1).split("/")[1]
    test_int = int(test_str)
    
    # Question is can we get this int back into a zenoh selector for _time
    # Zenoh timestamps are made from the 64bit time AND session ID which should be UUID...
    # 
    zombie = zenoh.Timestamp()
    sdfafs = zombie == test_t_1
    print(test)