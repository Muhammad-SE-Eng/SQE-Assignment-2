import subprocess
dot = r'''
digraph CFG { rankdir=TB; node [fontname="Arial", fontsize=10];
Start [shape=oval,label="Start"]; Exit [shape=oval,label="Exit"];
d1 [shape=diamond,label="d1\ndues < 0 ?"];
d2 [shape=diamond,label="d2\nnot(0<=enrolled<=cap)\nor cap<1 ?"];
d3 [shape=diamond,label="d3\ndues > 1000 ?"];
d4 [shape=diamond,label="d4\ncode in registered ?"];
d5 [shape=diamond,label="d5\nprereqs not satisfied ?"];
d6 [shape=diamond,label="d6\ncredit limit fails ?"];
d7 [shape=diamond,label="d7\nenrolled > capacity ?"];
E1 [shape=box,style=filled,fillcolor="#f8d7da",label="N9: raise\nInvalid dues"];
E2 [shape=box,style=filled,fillcolor="#f8d7da",label="N10: raise\nInvalid capacity/enrollment"];
R1 [shape=box,style=filled,fillcolor="#d1e7dd",label="N11: return DUES_BLOCK"];
R2 [shape=box,style=filled,fillcolor="#d1e7dd",label="N12: return ALREADY_REGISTERED"];
R3 [shape=box,style=filled,fillcolor="#d1e7dd",label="N13: return PREREQUISITES_MISSING"];
R4 [shape=box,style=filled,fillcolor="#d1e7dd",label="N14: return CREDIT_LIMIT"];
R5 [shape=box,style=filled,fillcolor="#d1e7dd",label="N15: return WAITLISTED"];
R6 [shape=box,style=filled,fillcolor="#d1e7dd",label="N16: return REGISTERED"];
Start->d1; d1->E1[label="T"]; d1->d2[label="F"];
d2->E2[label="T"]; d2->d3[label="F"];
d3->R1[label="T"]; d3->d4[label="F"];
d4->R2[label="T"]; d4->d5[label="F"];
d5->R3[label="T"]; d5->d6[label="F"];
d6->R4[label="T"]; d6->d7[label="F"];
d7->R5[label="T"]; d7->R6[label="F"];
E1->Exit; E2->Exit; R1->Exit; R2->Exit; R3->Exit; R4->Exit; R5->Exit; R6->Exit;
labelloc="t"; label="CFG of registration_decision()   N=17, E=23, V(G)=E-N+2=8";
}'''
open('docs/cfg.dot','w').write(dot)
subprocess.run(['dot','-Tpng','-Gdpi=130','docs/cfg.dot','-o','docs/cfg.png'],check=True)
