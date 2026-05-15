import java.util.*;

public class Main {
    static class StudentEnv {
        Map<String,Double> skills = new HashMap<>();
        StudentEnv(){
            skills.put("algebra",0.5);
            skills.put("geometry",0.4);
            skills.put("probability",0.3);
            skills.put("sequences",0.35);
        }
        Result step(String ex){
            double acc = skills.get(ex);
            boolean success = Math.random() < acc;
            double reward = success?1:-1;
            if(success) skills.put(ex, Math.min(1.0, acc+0.05));
            else skills.put(ex, Math.max(0.0, acc-0.02));
            return new Result(reward, success, skills.get(ex));
        }
    }
    static class Result {
        double reward; boolean success; double newSkill;
        Result(double r, boolean s, double ns){reward=r;success=s;newSkill=ns;}
    }
    static class RLAgent {
        Map<String,Double> q = new HashMap<>();
        double alpha=0.1, gamma=0.9;
        RLAgent(List<String> exs){ for(String e:exs) q.put(e,0.0); }
        String choose(){
            if(Math.random()>0.2) return Collections.max(q.entrySet(),Map.Entry.comparingByValue()).getKey();
            List<String> keys=new ArrayList<>(q.keySet());
            return keys.get(new Random().nextInt(keys.size()));
        }
        void update(String ex,double reward){
            double old=q.get(ex);
            q.put(ex, old+alpha*(reward+gamma*old-old));
        }
    }
    public static void main(String[] args){
        StudentEnv env=new StudentEnv();
        RLAgent agent=new RLAgent(Arrays.asList("algebra","geometry","probability","sequences"));
        for(int i=1;i<=30;i++){
            String ex=agent.choose();
            Result r=env.step(ex);
            agent.update(ex,r.reward);
            System.out.printf("Step %d: %s | Success=%s | Reward=%.1f | Skill=%.2f%n",
                              i,ex,r.success,r.reward,r.newSkill);
        }
    }
}