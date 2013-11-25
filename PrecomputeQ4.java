import java.io.*;
import java.util.*;

import org.apache.hadoop.hbase.HBaseConfiguration;
import org.apache.hadoop.hbase.client.Get;
import org.apache.hadoop.hbase.client.HTable;
import org.apache.hadoop.hbase.client.Put;
import org.apache.hadoop.hbase.client.Result;
import org.apache.hadoop.hbase.client.ResultScanner;
import org.apache.hadoop.hbase.client.Scan;
import org.apache.hadoop.hbase.util.Bytes;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.hbase.KeyValue;


// Class that has nothing but a main.
// Does a Put, Get and a Scan against an hbase table.
public class PrecomputeQ4 {
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
        
        //String[] table = new String[5];
        //String[] key = new String[5];
        //String[] column_f = new String[5];
        //String[] qualifier = new String[5];
        //String[] value = new String[5];
        //HTable[] htable = new HTable[5];
        //int tb_index;
        //int tb_cnt;

        //if (params.get("table_index").equals("all")) {
        //    tb_cnt = 3;
        //    tb_index = 2;
        //} else {
        //    tb_cnt = 1;
        //    tb_index = Integer.parseInt(params.get("table_index"));
        //}

        /* read hbase config */
        Configuration config = HBaseConfiguration.create();
	config.addResource("conf/hbase-site.xml");

        BufferedWriter bw = new BufferedWriter(new FileWriter(params.get("savetb4to")));

        HTable table = new HTable(config, "tb4");
        Scan scann = new Scan();
        scann.addFamily(Bytes.toBytes("usr"));
        ResultScanner scanner = table.getScanner(scann);

        long startTime = System.currentTimeMillis() / (1000);
        try {
            int i = 0;
            for (Result rr : scanner) {
                Long key = Bytes.toLong(rr.getRow());
                rr.size();
                
                //System.out.println("row " + Bytes.toLong(rr.getRow()) + " " + rr.size());
                //System.out.println(rr);
                bw.write("SET " + key + " ");
                List<KeyValue> kv = rr.list();
                for (int j = 0; j < kv.size(); j++) {
                    bw.write(Bytes.toLong(kv.get(j).getQualifier()) + ",");
                }

                bw.write("\n");
                
                //System.out.println(rr.list());
                //bw.write("SET " + key + " " + cnt + "\n");
                
                if ((++i) % 100000 == 0) {
                    long endTime = System.currentTimeMillis() / (1000);
                    System.out.print("finish " + i + " lines");
                    System.out.println(" time: "
                                       + (endTime - startTime)/3600 + "h:"
                                       + ((endTime - startTime)/60)%60 + "m:"
                                       + (endTime - startTime)%60 + "s");
                }

            }
        } finally {
            scanner.close();
            bw.close();
        }
    }
}
