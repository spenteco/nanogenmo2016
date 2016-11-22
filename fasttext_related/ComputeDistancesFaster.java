import java.io.*;
import java.util.*;
import java.text.DecimalFormat;
import java.text.NumberFormat;

public class ComputeDistancesFaster {
	
	public static void main(String[] args) {
		
		String INPUT_FILE = "/home/spenteco/0/pg_020516/pg.vec";
		String OUTPUT_FILE = "/home/spenteco/0/pg_020516/pg.distances.closest_distances";
		
		int NUMBER_OF_OUTPUT_WORDS = 15 + 1;			// ADD ONE BECAUSE WE DROP THE FIRST ONE, WHICH HAS A DISTANCE OF ZERO.
		
		DecimalFormat formatter = new DecimalFormat("0000.0000");
		
		try {
		
			File fin = new File(INPUT_FILE);	
		
			BufferedReader br = new BufferedReader(new FileReader(fin));
			
			HashMap<String, ArrayList> pgVectors = new HashMap<String, ArrayList>();
			
			String line = null;
			int n_read = 0;
			while ((line = br.readLine()) != null) {
				
				n_read += 1;
				
				if (n_read > 1) {
					
					String [] cols = line.split(" ");
					
					if (cols.length > 0) {
						
						String word = cols[0];
							
						ArrayList<Double> vec = new ArrayList<Double>();
						
						for (int a = 1; a < cols.length; a++) {
							vec.add(Double.valueOf(cols[a]));
						}
						
						pgVectors.put(word, vec);
					}
				}
			}
		 
			br.close();
			
			System.out.println("MESSAGE Loaded vectors");
			
			OutputStreamWriter writer = new OutputStreamWriter(new FileOutputStream(OUTPUT_FILE), "UTF-8");
			
			int n_processed = 0;
			
			for (String a : pgVectors.keySet()) {
				
				long startTime = System.currentTimeMillis();
				
				ArrayList<Double> vecA = pgVectors.get(a);
				ArrayList<String> results = new ArrayList<String>();
				
				for (String b : pgVectors.keySet()) {
						
					double d = 0.0;
					
					ArrayList<Double> vecB = pgVectors.get(b);
					
					for (int c = 0; c < vecA.size(); c++) {
						d = d + Math.abs(vecA.get(c) - vecB.get(c));
						if (d > 19.0) {
							break;
						}
					}
					
					if (d < 19.0) {
						results.add(formatter.format(d) + " " + a + " " + b);
					}
				}
				
		        Collections.sort(results);
		        
		        int i = 1;
		        while (i < NUMBER_OF_OUTPUT_WORDS && i < results.size()) {
					String [] cols = results.get(i).split(" ");
					writer.write(cols[1] + "\t" + cols[2] + "\t" + cols[0] + "\n");
					i = i + 1;
				}
			
				n_processed += 1;
				
				long endTime = System.currentTimeMillis();
				
				System.out.println("INFO processed " + n_processed + " " + a + 
									" time: " + (endTime - startTime) + 
									" results.size() " + results.size());
			}
			
			writer.close();
			
			System.out.println("INFO Done looping");
			
		}
		catch (Exception e) {
			System.out.println("ERROR " + e.getMessage());
			e.printStackTrace();
		}
	}
}
