import gurobi.*;
public class GurobiPoolV2 {

	  public static void main(String[] args) {
		    try {

/*		        double[][] reqLocations = {
		                {15.0,17.0,19.0,25.0,29.0,29.0,32.0,37.0,44.0,44.0,58.0,58.0,68.0,73.0,80.0,80.0,82.0},
		                {54.0,23.0,77.0,7.0,73.0,87.0,40.0,17.0,57.0,61.0,12.0,35.0,87.0,65.0,17.0,50.0,73.0}
		        };
		        double profit[] = new double[] {60.0,40.0,90.0,30.0,100.0,110.0,70.0,50.0,100.0,100.0,70.0,90.0,150.0,130.0,90.0,130.0,150.0};

	        double[][] poolLocations = {
		                {20.0,20.0,20.0,50.0,50.0,50.0,80.0,80.0,80.0,100.0},
		                {20.0,50.0,80.0,20.0,50.0,80.0,20.0,50.0,80.0,100.0}
		        };
		        double poolCapacity[] = new double[] {1.0, 1.0, 2.0, 2.0, 3.0, 3.0, 3.0, 3.0, 4.0, 3.0};
		        double costJ[] = new double[] {3.0, 3.0, 5.0, 5.0, 6.0, 6.0, 6.0, 6.0, 8.0, 8.0};
*/
		        
		        double[][] reqLocations = {
		                {15,17,19,25,29,29,32,37,44,44,58,58,68,73,80,80,82},
		                {54,23,77,7,73,87,40,17,57,61,12,35,87,65,17,50,73}
		        };
		        double profit[] = new double[] {60,40,90,30,100,110,70,50,100,100,70,90,150,130,90,130,150};
		          
		        //'locations' of the possible pool configurations in the same X-Y space
		        //(100,100) is the top right, and so 100 is the maximum request for either X or Y
		        double[][] poolLocations = {
		                {20,20,20,50,50,50,80,80,80,100},
		                {20,50,80,20,50,80,20,50,80,100}
		        };
		        double poolCapacity[] = new double[] {1, 1, 2, 2, 3, 3, 3, 3, 4, 4};
		        double costJ[] = new double[] {3, 3, 5, 5, 6, 6, 6, 6, 8, 10};

		        int numRequests = reqLocations[0].length;		//17; //reqLocations.length;
        		int numPools = poolLocations[0].length; 		//10;    //poolLocations.length;
        		System.out.println(numRequests+" "+numPools);
        		double[][] xjp = new double[numRequests][numPools];
  
        		for (int j = 0; j < numRequests; j++) {
        	        for (int p = 0; p < numPools; p++) {
        	        	if (reqLocations[0][j] <= poolLocations[0][p] && reqLocations[1][j] <= poolLocations[1][p]) {
        	              xjp[j][p] = 1;
        	            }
//        	            else {
//        	            	xjp[j][p] = 0;
//        	            }
        	        }
        	    }
/*        		for (int j = 0; j < numRequests; ++j) {
			        for (int p = 0; p < numPools; ++p) {
			        	System.out.print(xjp[j][p]+" ");
			        }
			        System.out.println();
        		}
*/        		
  		      // compute Waste
  		      
  		      double[][] wastejp = new double[numRequests][numPools];    
  		      double [][] valuejp = new double[numRequests][numPools];    
  		      for (int req = 0; req < numRequests; req++) {
  		         for (int pool = 0; pool < numPools; pool++) {
  		            if (reqLocations[0][req] <= poolLocations[0][pool] && reqLocations[1][req] <= poolLocations[1][pool]) {
  		               wastejp[req][pool] = (poolLocations[0][pool] - reqLocations[0][req]) + (poolLocations[1][pool] - reqLocations[1][req]);
  		               valuejp[req][pool] = profit[req]-wastejp[req][pool]-costJ[pool];
  		            }
  		            else {
  		               wastejp[req][pool] = 0;
  		               valuejp[req][pool] = 0;
  		            }
  		         }
  		      }
        	    
		      // Model
		      GRBEnv env = new GRBEnv();
		      GRBModel model = new GRBModel(env);
		      model.set(GRB.StringAttr.ModelName, "Pool Assignment");
		     
		      GRBVar[][] assign = new GRBVar[numRequests][numPools];
		      for (int j = 0; j < numRequests; ++j) {
		        for (int p = 0; p < numPools; ++p) {
		          assign[j][p] =
		              model.addVar(0, xjp[j][p], valuejp[j][p], GRB.BINARY,
		                           "assign" + j + "." + p);
		        }
		      }
		      
		      
/*		      GRBVar[][] waste = new GRBVar[numRequests][numPools];
		      for (int j = 0; j < numRequests; ++j) {
		        for (int p = 0; p < numPools; ++p) {
		          waste[j][p] =
		              model.addVar(0, wastejp[j][p], 0, GRB.CONTINUOUS,
		                           "waste" + j + "." + p);
		        }
		      }
*/		      
/*		      GRBVar cost[] = new GRBVar[numPools];
		      for (int j = 0; j < numRequests; ++j) {
		    	  for (int p = 0; p < numPools; ++p) {
		    		  cost[p]= 
		    				  model.addVar(0, xjp[j][p], costJ[p], GRB.CONTINUOUS,
		                           "Cost" +  p);
		    	  }
		      }
*/		      
		      
		      GRBLinExpr lhs;
		      
		      for (int j = 0; j < numRequests; ++j) {
		    	  lhs = new GRBLinExpr();
		    	  for (int p = 0; p < numPools; ++p) {
		    		  lhs.addTerm(1, assign[j][p]);
		  		  }
		  		  model.addConstr(lhs, GRB.EQUAL, 1, "PoolAssign");
		  	  }
		      
		      for (int p = 0; p < numPools; ++p) {
		  	 	lhs = new GRBLinExpr();
		  		for (int j = 0; j < numRequests; ++j) {
		  			lhs.addTerm(1, assign[j][p]);
		  		}
		  		model.addConstr(lhs, GRB.LESS_EQUAL, poolCapacity[p], "PoolCapacity");
		  	  }
/*		    
//		      GRBQuadExpr qobj = new GRBQuadExpr();
		      GRBLinExpr lobj = new GRBLinExpr();
	  		  for (int j = 0; j < numRequests; ++j) {
//	  			  qobj = new GRBQuadExpr();
	  			  lobj = new GRBLinExpr();
	  			  for (int p = 0; p < numPools; ++p) {
	  				  lobj.addTerm(wastejp[j][p], assign[j][p]);
//	  				  qobj.addTerm(1, waste[j][p],assign[j][p]);
	  			  }	  
	  		  } */
// For profit and cost
/*
		     GRBLinExpr l3obj = new GRBLinExpr();
	  		 for (int j = 0; j < numRequests; ++j) {
	  			  l3obj = new GRBLinExpr();
	  			  for (int p = 0; p < numPools; ++p) {
	  				  l3obj.addTerm(profit[p], assign[j][p]);
	  			  }	  
	  		 }
	  		  
	  		 for (int j = 0; j < numRequests; ++j) {
	  			  l3obj = new GRBLinExpr();
	  			  for (int p = 0; p < numPools; ++p) {
	  				  l3obj.addTerm(-costJ[p], assign[j][p]);
	  			  }	  
	  		 }

	  		  for (int j = 0; j < numRequests; ++j) {
	  			  l3obj = new GRBLinExpr();
	  			  for (int p = 0; p < numPools; ++p) {
	  				  l3obj.addTerm(-wastejp[j][p], assign[j][p]);
	  			  }	  
	  		  }
*/	  		
	  		  
		  	  // The objective is to minimize the total fixed and variable costs
//		      model.set(GRB.IntAttr.ModelSense, GRB.MINIMIZE);
		      model.set(GRB.IntAttr.ModelSense, GRB.MAXIMIZE);
		      //model.setObjective(lobj);
//		      model.setObjective(l3obj);
		      // Solve
		      model.set(GRB.IntParam.Method, GRB.METHOD_BARRIER);

		      model.optimize();

		      // Print solution
		      System.out.println("SOLUTION:");
//		      System.out.println(qobj.getValue());
		      double w=0;
		      double pr=0,c=0;
		      double v=0;
		      for (int j = 0; j < numRequests; ++j) {
		          for (int p = 0; p < numPools; ++p) {
 		            if (assign[j][p].get(GRB.DoubleAttr.X) > 0.00000000001) {
		            	w=w+wastejp[j][p];
		            	c=c+costJ[p];
		            	pr=pr+profit[p];
		            	v=v+valuejp[j][p];
		            	System.out.println(j+","+p+":"+assign[j][p].get(GRB.DoubleAttr.X));
//		            	System.out.println(j+","+p+" waste:"+waste[j][p].get(GRB.DoubleAttr.X)+"*assign"+assign[j][p].get(GRB.DoubleAttr.X));
		            }
		          }
		      } 
		      System.out.println("Value "+v);
  		      for (int j = 0; j < numRequests; ++j) {
  		    	  for (int p = 0; p < numPools; ++p) {
  		    		  System.out.print(valuejp[j][p]+" ");
  		    	  }
  		    	  System.out.println();
  		      }

		      // Dispose of model and environment
		      model.dispose();
		      env.dispose();

		    } catch (GRBException e) {
		      System.out.println("Error code: " + e.getErrorCode() + ". " +
		          e.getMessage());
		    }
		  }
		}