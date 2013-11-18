import java.io.IOException;
import java.io.FileReader;
import java.io.BufferedReader;
import java.util.Map;
import java.util.HashMap;
import java.util.Scanner;

import com.google.gson.JsonParser;
import com.google.gson.Gson;
import com.google.gson.reflect.TypeToken;

import org.apache.hadoop.hbase.HBaseConfiguration;
import org.apache.hadoop.hbase.client.Get;
import org.apache.hadoop.hbase.client.HTable;
import org.apache.hadoop.hbase.client.Put;
import org.apache.hadoop.hbase.client.Result;
import org.apache.hadoop.hbase.client.ResultScanner;
import org.apache.hadoop.hbase.client.Scan;
import org.apache.hadoop.hbase.util.Bytes;
import org.apache.hadoop.conf.Configuration;


// Class that has nothing but a main.
// Does a Put, Get and a Scan against an hbase table.
public class loadData {
    public static void main(String[] args) throws IOException {

        /* read table info from config */
        Map<String, String> params = new HashMap<String, String>();
        Scanner scan = new Scanner(new FileReader(args[0]));
        String line = null;
        do {
            line = scan.nextLine();
            if (line.length() > 0) {
                String[] pair = line.split(":");
                params.put(pair[0].trim(), pair[1].trim());
            }
        } while (scan.hasNext());
        
        String[] table = new String[5];
        String[] key = new String[5];
        String[] column_f = new String[5];
        String[] qualifier = new String[5];
        String[] value = new String[5];
        HTable[] htable = new HTable[5];
        int tb_index;
        int tb_cnt;

        if (params.get("table_index").equals("all")) {
            tb_cnt = 3;
            tb_index = 2;
        } else {
            tb_cnt = 1;
            tb_index = Integer.parseInt(params.get("table_index"));
        }

        /* read hbase config */
        Configuration config = HBaseConfiguration.create();
	config.addResource("conf/hbase-site.xml");
        for (int i = 0; i < tb_cnt; i++) {
            table[tb_index+i] = params.get("table_" + (tb_index+i));
            key[tb_index+i] = params.get("key_" + (tb_index+i));
            column_f[tb_index+i] = params.get("column_f_" + (tb_index+i));
            qualifier[tb_index+i] = params.get("qualifier_" + (tb_index+i));
            value[tb_index+i] = params.get("value_" + (tb_index+i));
            htable[tb_index+i] = new HTable(config, table[tb_index+i]);

        }

        for (int i = 0; i < tb_cnt; i++) {
            System.out.println(table[tb_index+i] + " "
                               + key[tb_index+i] + " "
                               + column_f[tb_index+i] + " "
                               + qualifier[tb_index+i] + " "
                               + value[tb_index+i]);
        }
        

        /* iterate on each json file from the list */
        BufferedReader brr = new BufferedReader(new FileReader(params.get("json_list")));
        String json_file = null;
        long totalstartTime = System.currentTimeMillis() / (1000);
        while (null != (json_file = brr.readLine())) {
            /* read json data and put */
            BufferedReader br = new BufferedReader(new FileReader(json_file));
            line = null;
            int count = 0;
            long startTime = System.currentTimeMillis() / (1000);
            while (null != (line = br.readLine())) {
                //System.out.println(line);
                Gson gson = new Gson();
                Map<String, String> map = gson.fromJson(line,
                                                        new TypeToken<Map<String, String>>() {}.getType());
                //System.out.println("rt: " + map.get("rt"));

                for (int i = 0; i < tb_cnt; i++) {
                    /* test if no retweet id */
                    if (!map.containsKey(key[tb_index+i])) {
                        continue;
                    }

                    Put p = new Put(Bytes.toBytes(Long.parseLong(map.get(key[tb_index+i]))));
                    String fValue;
                    if (value[tb_index+i].equals("null")) {
                        fValue = "1";
                    } else {
                        fValue = map.get(value[tb_index+i]);
                    }
                
                    p.add(Bytes.toBytes(column_f[tb_index+i]),
                          Bytes.toBytes(Long.parseLong(map.get(qualifier[tb_index+i]))),
                          Bytes.toBytes(fValue));
            
                    htable[tb_index+i].put(p);
                }
            
                count++;
                if (count % 1000 == 0) {
                    System.out.println("line " + count);
                }
            }
        
            long endTime = System.currentTimeMillis() / (1000);
            System.out.println("Done! " + json_file + " time spent: " + (endTime - startTime) + "s");
        }

        long totalendTime = System.currentTimeMillis() / (1000);
        System.out.println("Done All files! " + "total time: "
                           + (totalendTime - totalstartTime)/3600 + "h:"
                           + (totalendTime - totalstartTime)%60 + "m:"
                           + (totalendTime - totalstartTime)%60 + "s");
    }
}
