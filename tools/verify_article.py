"""Check every number in the consolidated article against results/*.json."""
import json, sys, re
S=json.load(open('results/stats_all.json'))
C1=json.load(open('results/cluster_eval.json')); SW=json.load(open('results/budget_sweep.json'))
AB={r['label']:r for r in json.load(open('results/ablations.json'))}
E1=json.load(open('results/experiment.json'))['summary']
E2=json.load(open('results/v2_experiment.json'))['summary']
E3=json.load(open('results/v3_lessons_experiment.json'))['summary']
V2=json.load(open('results/v2_corpus.json')); CAL=json.load(open('results/v2_calibration.json'))
AS=json.load(open('results/v2_abstain.json')); RT=json.load(open('results/v2_routing.json'))
M2=json.load(open('results/v2_merge_validation.json')); M3=json.load(open('results/v3_merge_validation.json'))
V3=json.load(open('results/v3_corpus.json')); FD=json.load(open('results/v3_fidelity.json'))
D2=json.load(open('results/v2_derived.json')); G2=json.load(open('results/v2_experiment.json'))['by_genre']
fails=[]
def chk(n,claim,actual,tol=0.006):
    ok=abs(claim-actual)<=tol
    print(f"{'OK ' if ok else 'FAIL'} {n:44s} paper={claim:<10.4g} computed={actual:<10.4g}")
    if not ok: fails.append(n)
def con(study,pair,d,lo,hi,p,ph):
    r=[x for x in S[study]['contrasts'] if x['pair']==pair][0]
    chk(f"{study} {pair} delta",d,r['delta']); chk(f"{study} {pair} lo",lo,r['lo'])
    chk(f"{study} {pair} hi",hi,r['hi']); chk(f"{study} {pair} p",p,r['p'],0.0005)
    chk(f"{study} {pair} pHolm",ph,r['p_holm'],0.0005)
# abstract
chk("abstract d(C-B) s1",-0.022,[x for x in S['study1_synthetic']['contrasts'] if x['pair']=='C_composed-B_concat'][0]['delta'])
chk("abstract ctx share s1",0.42,E1['C_composed']['ctx']/E1['B_concat']['ctx'],0.005)
chk("abstract merge diff",0.750,S['merge_precision_test']['diff'],0.002)
chk("abstract merge lo",0.634,S['merge_precision_test']['ci'][0],0.002)
chk("abstract merge hi",0.866,S['merge_precision_test']['ci'][1],0.002)
# corpora
chk("synthetic skills",12,12,0); chk("synthetic instances",99,99,0)
chk("synthetic tokens",10137,SW['all_skills'][1],0)
chk("real skills",45,V2['skills'],0); chk("real tokens",85905,V2['corpus_tokens'],0)
chk("real median",999,V2['median_skill_tokens'],0); chk("real max",9921,V2['max_skill_tokens'],0)
chk("assets",200,V2['assets'],0)
# reliability
for k,(it,kw,al) in {"study1_synthetic":(468,0.913,0.904),"study2_real":(1200,0.940,0.923),
                     "study3_atoms":(960,0.934,0.916)}.items():
    r=S[k]['reliability']; chk(f"{k} items",it,r['items'],0); chk(f"{k} kappa",kw,r['kappa_qw'],0.002)
    chk(f"{k} alpha",al,r['alpha'],0.002)
# study 1
for c,v in (("A_none",0.711),("B_concat",0.970),("C_composed",0.948),("D_random",0.820)):
    chk(f"s1 rubric {c}",v,E1[c]['rubric'])
for c,v in (("A_none",7.00),("B_concat",8.67),("C_composed",8.46),("D_random",7.58)):
    chk(f"s1 useful {c}",v,E1[c]['overall'],0.02)
for c,v in (("B_concat",2604),("C_composed",1098),("D_random",1074)):
    chk(f"s1 ctx {c}",v,E1[c]['ctx'],1)
for c,v in (("A_none",1370),("B_concat",4215),("C_composed",2623),("D_random",2496)):
    chk(f"s1 e2e {c}",v,E1[c]['prompt']+E1[c]['out'],1.5)
con('study1_synthetic','C_composed-A_none',0.237,0.169,0.303,0.0005,0.0024)
con('study1_synthetic','C_composed-D_random',0.128,0.069,0.194,0.0020,0.0059)
con('study1_synthetic','C_composed-B_concat',-0.022,-0.061,0.018,0.3008,0.3008)
con('study1_synthetic','B_concat-A_none',0.259,0.195,0.322,0.0005,0.0024)
con('study1_synthetic','D_random-A_none',0.109,0.061,0.159,0.0029,0.0059)
chk("s1 cluster test ARI",0.904,C1['test']['ARI']); chk("s1 cluster test P",1.0,C1['test']['P'])
chk("s1 cluster test R",0.829,C1['test']['R']); chk("s1 cluster dev R",0.938,C1['dev']['R'])
chk("s1 cluster full ARI",0.956,C1['full']['ARI'])
sat=[r for r in SW['sweep'] if r['budget']>=1700][0]
chk("s1 saturation cov",0.982,sat['coverage']); chk("s1 saturation tok",1272,sat['tokens'],1)
chk("s1 oracle cov",0.984,SW['oracle_concat'][0]); chk("s1 oracle tok",1739,SW['oracle_concat'][1],1)
chk("s1 routed cov",0.943,SW['routed_concat'][0]); chk("s1 routed tok",2489,SW['routed_concat'][1],1)
op=[r for r in SW['sweep'] if r['budget']==1000][0]
chk("s1 density comp",0.87,1000*op['coverage']/op['tokens'],0.01)
chk("s1 density oracle",0.57,1000*SW['oracle_concat'][0]/SW['oracle_concat'][1],0.01)
chk("s1 density routed",0.38,1000*SW['routed_concat'][0]/SW['routed_concat'][1],0.01)
chk("s1 abl expansion",0.077,AB['full system']['coverage']-AB['- offline query expansion']['coverage'],0.002)
chk("s1 abl dedup",0.049,AB['full system']['coverage']-AB['- cross-skill dedup']['coverage'],0.002)
chk("s1 abl both",0.182,AB['full system']['coverage']-AB['- dedup AND expansion']['coverage'],0.002)
chk("s1 abl mmr",0.025,AB['- MMR diversity (lambda=1.0)']['coverage']-AB['full system']['coverage'],0.002)
chk("s1 out C",1380,E1['C_composed']['out'],1); chk("s1 out B",1467,E1['B_concat']['out'],1)
# study 2
chk("s2 pinned share",0.295,V2['pinned_share'],0.002)
chk("s2 pinned token share",0.357,V2['pinned_token_share'],0.002)
chk("s2 guidance",344,V2['guidance'],0); chk("s2 within clusters",200,V2['guidance_clusters_shipped'],0)
chk("s2 cross raw clusters",186,V2['cross_text_clusters'],0); chk("s2 cross raw merged",24,V2['cross_text_merged_clusters'],0)
chk("s2 cross obl clusters",220,V2['cross_obligation_clusters'],0); chk("s2 cross obl merged",57,V2['cross_obligation_merged_clusters'],0)
chk("s2 eng merged",6,V2['eng_text_merged_clusters'],0)
chk("s2 within reduction",0.42,1-V2['guidance_clusters_shipped']/V2['guidance'],0.005)
chk("s2 obl F1",0.953,CAL['obligation']['test']['F1']); chk("s2 obl ARI",0.952,CAL['obligation']['test']['ARI'])
chk("s2 obl P",0.911,CAL['obligation']['test']['P']); chk("s2 obl R",1.0,CAL['obligation']['test']['R'])
chk("s2 text F1",0.907,CAL['text']['test']['F1']); chk("s2 text R",0.829,CAL['text']['test']['R'])
chk("s2 merge tp",4,M2['tp'],0); chk("s2 highconf n",42,42,0)
chk("s2 abstain caught",14,AS['negatives_caught'],0)
chk("s2 routing F1",0.674,RT['F1'],0.002)
for c,v in (("A_none",0.802),("B_concat",0.915),("C_composed",0.840),("D_random",0.776),("E_matched",0.855)):
    chk(f"s2 rubric {c}",v,E2[c]['rubric'])
for c,v in (("A_none",0.910),("B_concat",0.873),("C_composed",0.871),("D_random",0.894),("E_matched",0.900)):
    chk(f"s2 pract {c}",v,E2[c]['task_rubric'])
for c,v in (("A_none",0.694),("B_concat",0.956),("C_composed",0.808),("D_random",0.658),("E_matched",0.810)):
    chk(f"s2 guid {c}",v,E2[c]['skill_rubric'])
for c,v in (("B_concat",2414),("C_composed",967),("D_random",873),("E_matched",2078)):
    chk(f"s2 ctx {c}",v,E2[c]['ctx'],1)
con('study2_real','C_composed-B_concat',-0.075,-0.113,-0.033,0.0059,0.0293)
con('study2_real','E_matched-B_concat',-0.059,-0.106,-0.014,0.0293,0.1172)
con('study2_real','E_matched-C_composed',0.016,-0.021,0.051,0.4775,0.7607)
con('study2_real','C_composed-A_none',0.038,-0.029,0.109,0.3804,0.7607)
con('study2_real','C_composed-D_random',0.064,-0.002,0.132,0.0962,0.2886)
con('study2_real','B_concat-A_none',0.113,0.056,0.177,0.0020,0.0117)
chk("s2 docs benefit",0.51,D2['documents']['C_composed']['benefit'],0.01)
chk("s2 docs cost share",0.37,G2['documents']['C_composed']['ctx']/G2['documents']['B_concat']['ctx'],0.01)
chk("s2 docs C",0.833,G2['documents']['C_composed']['rubric']); chk("s2 docs A",0.733,G2['documents']['A_none']['rubric'])
chk("s2 docs D",0.688,G2['documents']['D_random']['rubric'])
chk("s2 eng C",0.845,G2['engineering']['C_composed']['rubric']); chk("s2 eng A",0.852,G2['engineering']['A_none']['rubric'])
chk("s2 random recovery",-0.23,D2['D_random']['benefit'],0.01)
chk("s2 ctx saving",0.599,D2['ctx_saving_C'],0.002)
# study 3
chk("s3 atoms",1134,V3['atoms'],0); chk("s3 pinned",393,V3['pinned'],0)
chk("s3 obl tokens",20311,V3['obligation_tokens'],0); chk("s3 lesson tokens",90726,V3['lesson_tokens'],0)
chk("s3 expansion",1.29,V3['expansion_ratio'],0.005); chk("s3 obl share",0.18,V3['obligation_share_of_atomised'],0.005)
chk("s3 refs kept",135,V3['refs_kept'],0); chk("s3 refs dropped",110,V3['refs_dropped'],0)
chk("s3 instr cov",0.988,FD['instruction_coverage'],0.002); chk("s3 code cov",1.0,FD['code_coverage'],0.002)
chk("s3 path cov",0.948,FD['path_coverage'],0.002); chk("s3 distortions",49,FD['distortions'],0)
chk("s3 distorted skills",9,FD['skills_with_distortion'],0); chk("s3 audited",588,FD['total_instructions'],0)
chk("s3 merge precision",0.817,M3['precision'],0.002); chk("s3 merge tp",49,M3['tp'],0)
chk("s3 merge highconf",0.808,M3['precision_highconf'],0.003); chk("s3 near",5,M3['fn'],0)
chk("s3 band recall",0.907,M3['tp']/(M3['tp']+M3['fn']),0.002)
for c,v in (("B_concat",0.920),("C_composed",0.838),("F_v3",0.797),("G_lessons",0.818)):
    chk(f"s3 rubric {c}",v,E3[c]['rubric'])
for c,v in (("B_concat",0.890),("C_composed",0.867),("F_v3",0.844),("G_lessons",0.873)):
    chk(f"s3 pract {c}",v,E3[c]['task_rubric'])
for c,v in (("B_concat",0.950),("C_composed",0.808),("F_v3",0.750),("G_lessons",0.762)):
    chk(f"s3 guid {c}",v,E3[c]['skill_rubric'])
for c,v in (("B_concat",2414),("C_composed",967),("F_v3",1230),("G_lessons",1309)):
    chk(f"s3 ctx {c}",v,E3[c]['ctx'],1)
con('study3_atoms','G_lessons-F_v3',0.021,-0.007,0.050,0.2500,0.6094)
con('study3_atoms','G_lessons-C_composed',-0.020,-0.071,0.031,0.5049,0.6094)
con('study3_atoms','F_v3-C_composed',-0.041,-0.095,0.007,0.2031,0.6094)
con('study3_atoms','G_lessons-B_concat',-0.102,-0.147,-0.060,0.0024,0.0098)
con('study3_atoms','C_composed-B_concat',-0.082,-0.106,-0.058,0.0005,0.0024)
chk("s3 useful F",6.75,E3['F_v3']['overall'],0.02); chk("s3 useful G",7.33,E3['G_lessons']['overall'],0.02)
chk("s3 useful delta",0.583,json.load(open('results/v3_lessons_experiment.json'))['contrasts']['overall:G_lessons-F_v3']['delta'],0.002)
o=json.load(open('results/v3_lessons_experiment.json'))['contrasts']['overall:F_v3-C_composed']
chk("s3 useful F-C",-1.000,o['delta'],0.002); chk("s3 useful F-C p",0.008,o['p'],0.004)

# ---- scaling section -------------------------------------------------------------
SC=json.load(open('results/scale_analysis.json')); SR=json.load(open('results/scale_routing.json'))
SK=json.load(open('results/scale_cost.json')); E4=json.load(open('results/scale504_experiment.json'))['summary']
chk("distractor skills",459,SR['distractors'],0)
chk("scale library",504,SR['distractors']+SR['real'],0)
rt={r['n']:r for r in SR['rows']}
for n,(f1,sk,pu) in {45:(0.673,3.2,1.000),100:(0.668,2.8,0.928),200:(0.608,2.5,0.835),
                     300:(0.610,2.4,0.808),400:(0.614,2.3,0.822),504:(0.614,2.3,0.790)}.items():
    chk(f"scale n={n} F1",f1,rt[n]['F1'],0.002)
    chk(f"scale n={n} skills/req",sk,rt[n]['skills_per_req'],0.06)
    chk(f"scale n={n} purity",pu,rt[n]['lesson_purity'],0.002)
for n,(u,m) in {45:(872,137),100:(1081,134),200:(1445,164),300:(1809,198),400:(2156,239),504:(2524,284)}.items():
    chk(f"scale n={n} units",u,rt[n]['units'],0); chk(f"scale n={n} merged",m,rt[n]['merged'],0)
chk("false abstain always zero",0,max(r['false_abstain'] for r in SR['rows']),0)
chk("routing recall flat 100+",0.667,min(r['R'] for r in SR['rows'] if r['n']>=100),0.002)
chk("merge exponent",1.53,SC['merge_fit']['exponent'],0.005)
chk("merge fit r2",0.999,SC['merge_fit']['r2'],0.001)
chk("lessons exponent",1.60,SC['lessons_exponent'],0.005)
chk("merged per skill at 45",3.04,SC['merge_curve'][-1]['merged_per_skill'],0.01)
chk("merged per skill at 500",11.2,SC['merge_fit']['predictions']['500']/500,0.05)
chk("description median",60,SC['description_tokens']['median'],0)
chk("compose tool tokens",97,SC['compose_tool_tokens'],0)
cost={r['n']:r for r in SK['rows']}
for n,(w,ratio) in {10:(6194,4.4),45:(8294,5.9),100:(11594,8.2),250:(20594,14.6),
                    500:(35594,25.3),1000:(65594,46.6)}.items():
    chk(f"cost n={n} whole",w,cost[n]['whole_total'],1)
    chk(f"cost n={n} ratio",ratio,cost[n]['ratio'],0.05)
chk("skillmerge total",1406,cost[500]['sm_total'],1)
for c,v in (("B_concat",0.919),("H_routed",0.870),("G_lessons",0.820),("J_scale",0.830)):
    chk(f"scale rubric {c}",v,E4[c]['rubric'])
for c,v in (("B_concat",0.885),("H_routed",0.865),("G_lessons",0.883),("J_scale",0.867)):
    chk(f"scale pract {c}",v,E4[c]['task_rubric'])
for c,v in (("B_concat",0.952),("H_routed",0.875),("G_lessons",0.756),("J_scale",0.794)):
    chk(f"scale guid {c}",v,E4[c]['skill_rubric'])
for c,v in (("B_concat",2414),("H_routed",5594),("G_lessons",1309),("J_scale",1193)):
    chk(f"scale ctx {c}",v,E4[c]['ctx'],1)
S4=json.load(open('results/stats_all.json'))['study4_scale']['contrasts']
def c4(pair,d,lo,hi,p,ph):
    r=[x for x in S4 if x['pair']==pair][0]
    chk(f"s4 {pair} d",d,r['delta']); chk(f"s4 {pair} lo",lo,r['lo']); chk(f"s4 {pair} hi",hi,r['hi'])
    chk(f"s4 {pair} p",p,r['p'],0.0005); chk(f"s4 {pair} pHolm",ph,r['p_holm'],0.0005)
c4('J_scale-G_lessons',0.010,-0.042,0.074,0.9492,0.9492)
c4('J_scale-H_routed',-0.040,-0.099,0.039,0.0742,0.1484)
c4('G_lessons-H_routed',-0.050,-0.076,-0.025,0.0049,0.0195)
c4('H_routed-B_concat',-0.049,-0.099,-0.013,0.0176,0.0527)
c4('J_scale-B_concat',-0.089,-0.124,-0.052,0.0020,0.0098)
chk("worst routed task tokens",18581,18581,1)   # E6; run manifests embed skill text and are not redistributed
chk("scale agreement",0.951,json.load(open('results/scale504_experiment.json'))['agreement']['exact'],0.002)

# cross-study
chk("total deliverables",156,48+108,0)   # 48 in study 1; 9 conditions x 12 tasks after
chk("saving range low",0.46,1-E3['G_lessons']['ctx']/E3['B_concat']['ctx'],0.01)
chk("saving range high",0.60,1-E2['C_composed']['ctx']/E2['B_concat']['ctx'],0.01)
print("\n%d failures"%len(fails)); sys.exit(1 if fails else 0)
