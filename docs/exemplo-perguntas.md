# Dataset de Perguntas Naturais - Tipster de Futebol Brasileiro (LLM+RAG)

Este arquivo contém perguntas em linguagem natural focadas em extrair dados da API-FOOTBALL para o contexto do futebol brasileiro (Séries A, B, C, Estaduais e Copas). O objetivo é cobrir clubes, jogadores, confrontos, odds, mercados, arbitragem e estratégia.

**Atualizações Recentes:**
- Bot agora inclui contexto de data atual em todas as respostas
- Sistema de odds integrado com simulação baseada em força dos times
- Suporte para integração com APIs reais de odds (The Odds API, etc.)

---

## 1) Partidas e calendário (Rodadas, Horários, Clássicos)

## 1) Partidas e calendário (Rodadas, Horários, Clássicos)
1. Quais jogos da Série A acontecem hoje?
2. Me mostre os jogos da Série B desta rodada.
3. Que partidas começam nas próximas 2 horas no Brasileirão?
4. Tem algum clássico paulista nesta semana?
5. Mostre todos os jogos do Flamengo neste mês.
6. Quais times estão jogando fora de casa neste fim de semana?
7. Me mostre os jogos do Campeonato Carioca desta semana.
8. Quais partidas têm times que estão na zona de rebaixamento?
9. Quais jogos podem ser decisivos para o título do Brasileirão?
10. Tem algum duelo de meio de tabela hoje?
11. Quais jogos da Série C estão marcados para amanhã?
12. Quais partidas estão programadas para quarta-feira à noite?
13. Existe algum jogo atrasado do Brasileirão que será realizado hoje?
14. Mostre os próximos 5 jogos do Atlético-MG.
15. Quais jogos da próxima rodada têm previsão de casa cheia?
16. Quais jogos do Campeonato Mineiro estão programados para hoje?
17. Tem algum jogo decisivo de rebaixamento nesta rodada?
18. Quais partidas têm times líderes contra últimos colocados?
19. Me mostre os jogos do Corinthians na temporada atual.
20. Quais partidas do Cruzeiro ainda não têm estádio definido?
21. Quais jogos do Flamengo estão transmitidos na TV hoje?
22. Tem algum jogo do Palmeiras com alta expectativa de público?
23. Quais partidas têm times com chance de classificação para Libertadores?
24. Me mostre os jogos de sábado e domingo do Brasileirão.
25. Quais times jogam fora de casa na rodada atual?
26. Qual jogo é mais provável de terminar empatado nesta rodada?
27. Existem partidas adiadas ou suspensas?
28. Quais jogos do Grêmio serão decisivos para rebaixamento?
29. Tem algum clássico regional nesta semana?
30. Me mostre os jogos de times paulistas na Série B.
31. Quais jogos têm previsão de mais de 2 gols?
32. Quais partidas têm arbitragem definida para hoje?
33. Quais clubes estão jogando em casa nos próximos 3 dias?
34. Tem algum jogo do Internacional com grande expectativa de público?
35. Quais partidas da Série A têm times líderes contra times do meio da tabela?
36. Quais jogos estão programados para horário noturno?
37. Quais partidas podem influenciar diretamente o rebaixamento?
38. Me mostre jogos com times invictos nesta rodada.
39. Quais jogos da Série B estão sendo transmitidos online?
40. Quais jogos têm clássicos locais nesta semana?
41. Quais times têm sequência de vitórias nos próximos jogos?
42. Qual jogo do Flamengo tem maior probabilidade de gols?
43. Me mostre os próximos 5 jogos do Santos.
44. Quais jogos do Botafogo são considerados de risco de rebaixamento?
45. Quais partidas da Série C têm times líderes?
46. Quais jogos têm previsão de chuva e podem afetar desempenho?
47. Quais partidas são consideradas decisivas para Libertadores?
48. Me mostre os jogos do Athletico-PR nesta rodada.
49. Quais jogos do Ceará têm times na zona de classificação?
50. Quais partidas do Fortaleza são contra times da parte de baixo da tabela?

## 2) Odds e Mercados (1X2, Over/Under, Handicaps, Valor)
51. Qual a odd para vitória do Palmeiras contra o Corinthians?
52. Me mostre todas as odds da próxima rodada do Brasileirão.
53. Existe algum mercado de Over/Under 2.5 gols nos próximos jogos?
54. Qual é a odd de empate do Botafogo contra o Fluminense?
55. Qual mercado oferece mais valor hoje no Brasileirão?
56. Algum jogo do Ceará ou Fortaleza apresenta value bet?
57. Como a odd da vitória do São Paulo mudou nas últimas 24 horas?
58. Quais odds dos principais bookmakers brasileiros estão divergentes?
59. Qual time está sendo subestimado pelas odds do mercado?
60. Alguma partida apresenta alta chance de gols no segundo tempo?
61. Quais jogos têm odds de draw no primeiro tempo superiores a 3.0?
62. Existe algum jogo com odds de over/under 1.5 muito altas?
63. Me mostre jogos com handicaps asiáticos favoráveis para azarões.
64. Qual odd do Flamengo para vencer sem sofrer gol?
65. Existe algum mercado de dupla chance interessante hoje?
66. Quais partidas apresentam odds interessantes para gols de ambos os times?
67. Me mostre apostas de escanteios acima de 9 no primeiro tempo.
68. Quais jogos têm apostas de cartões acima de 3,5 possíveis?
69. Qual jogo apresenta maior expectativa de gols no segundo tempo?
70. Me mostre apostas de gols por tempo (1T/2T) para o próximo jogo.
71. Quais jogos têm odds acima de 4.0 para zebra?
72. Existe algum mercado de gols exatos interessante?
73. Quais partidas têm odds de empate no intervalo atraentes?
74. Me mostre jogos com possibilidade de handicap +1 para azarões.
75. Quais jogos apresentam over/under 3.5 com alta probabilidade?
76. Qual odd do São Paulo para ganhar com handicap -1?
77. Existe algum mercado de total de escanteios acima de 10?
78. Me mostre jogos com apostas de cartões por equipe.
79. Quais jogos têm apostas de gols primeiro tempo/segundo tempo favoráveis?
80. Qual jogo apresenta melhor relação risco-retorno para apostas combinadas?

## 2.1) Odds com Contexto de Data (Novas Funcionalidades)
81. Qual a odd para vitória do Palmeiras hoje, considerando que estamos em novembro de 2025?
82. Me mostre as odds da rodada do fim de semana passado, já que hoje é segunda-feira.
83. Quais jogos acontecem amanhã e suas respectivas odds para vitória em casa?
84. Existe algum value bet nos jogos desta semana no Brasileirão?
85. Como as odds mudaram desde ontem para os jogos de hoje?
86. Qual seria a odd estimada para um clássico que acontecerá no próximo sábado?
87. Me mostre as odds simuladas para os próximos jogos do Flamengo neste mês.
88. Qual time tem odds mais favoráveis para vencer em casa nos jogos da próxima rodada?
89. Existe alguma oportunidade de aposta nos jogos que ocorrem depois de amanhã?
90. Como ficam as odds se considerarmos que hoje é um dia de semana sem jogos importantes?

## 3) Estatísticas de Clubes (Gols, Defesa, Posse, Escanteios)
91. Qual time tem mais vitórias fora de casa?
82. Qual clube tem a melhor defesa nos últimos 5 jogos?
83. Qual time marcou mais gols nos últimos 10 jogos?
84. Qual time sofre mais gols em casa?
85. Qual é a média de posse de bola do Atlético-MG neste campeonato?
86. Quais clubes têm maior média de finalizações certas por jogo?
87. Qual time brasileiro tem mais cartões vermelhos neste campeonato?
88. Qual time faz mais gols no segundo tempo?
89. Qual time tem mais escanteios por partida?
90. Qual time perde menos bolas na defesa?
91. Qual time tem melhor aproveitamento em bolas paradas ofensivas?
92. Qual time apresenta maior média de passes precisos por jogo?
93. Qual time possui maior taxa de conversão de finalizações em gols?
94. Qual clube sofre mais faltas por jogo?
95. Qual time tem maior média de chutes no alvo?
96. Qual time marca mais gols em casa nos últimos 5 jogos?
97. Qual time sofre menos gols fora de casa?
98. Qual clube tem melhor aproveitamento em confrontos diretos?
99. Qual time tem melhor aproveitamento em clássicos regionais?
100. Qual time possui maior média de escanteios favoráveis por jogo?

## 4) Performance de Jogadores (Player Props & Scouts)
110. Qual a média de chutes a gol do Hulk nas últimas 5 partidas?
102. O Gabigol costuma marcar contra o Vasco?
103. Quais jogadores do Palmeiras têm maior probabilidade de levar cartão amarelo hoje?
104. Quem é o líder de assistências do Flamengo na temporada?
105. Qual a odd para o Cano marcar a qualquer momento?
106. O goleiro do Corinthians tem média alta de defesas por jogo?
107. Raphael Veiga tem bom aproveitamento em pênaltis este ano?
108. Quais jogadores estão pendurados para a próxima rodada?
109. Mostre a média de desarmes dos volantes do Botafogo.
110. Qual jogador sofre mais faltas no Campeonato Brasileiro?
111. Tiquinho Soares marca mais gols em casa ou fora?
112. Quem são os cobradores de falta oficiais do São Paulo?
113. Qual a chance de Paulinho (Atlético-MG) marcar o primeiro gol do jogo?
114. Quantos passes para finalização o Arrascaeta fez no último jogo?
115. Existem jogadores com "Lei do Ex" ativa no jogo Santos x Palmeiras?
116. Qual zagueiro do Grêmio ganha mais duelos aéreos?
117. Quem tem a maior média de impedimentos na liga?
118. Qual jogador tem a maior sequência de jogos marcando gols atualmente?
119. Compare as estatísticas de finalização entre Calleri e Yuri Alberto.
120. Qual lateral cruza mais bolas na área no campeonato?

## 5) Arbitragem e Disciplina (Cartões e Faltas)
130. Quem apita o jogo do Flamengo hoje?
122. O árbitro escalado para o clássico tem média alta de cartões vermelhos?
123. Qual a média de cartões amarelos do Wilton Pereira Sampaio?
124. Esse juiz costuma dar muitos pênaltis?
125. Cruzeiro e Atlético-MG é um jogo com tendência para mais de 6 cartões?
126. Qual time reclama mais e leva cartões por indisciplina?
127. O árbitro de hoje deixa o jogo seguir ou para muito por faltas?
128. Qual a probabilidade de expulsão neste confronto baseada no histórico do juiz?
129. Times mandantes ganham mais com esse árbitro?
130. Quantos cartões o Fagner já tomou neste campeonato?

## 6) Tendências, Tabus e Histórico (H2H Avançado)
140. O São Paulo já venceu o Corinthians na Neo Química Arena?
132. Há quanto tempo o Internacional não ganha do Grêmio?
133. O Vasco costuma marcar gol quando joga em altitude ou fora de casa longe?
134. Qual é o retrospecto do Fortaleza jogando no Maracanã?
135. Existe algum tabu histórico no jogo entre Bahia e Vitória?
136. O Fluminense costuma perder jogos antes de decisões da Libertadores?
137. Como o Palmeiras joga logo após uma Data FIFA?
138. O Athletico-PR é forte jogando na Arena da Baixada em jogos noturnos?
139. Qual time tem o pior desempenho jogando às 11h da manhã?
140. O Cuiabá costuma marcar gols nos últimos 15 minutos de jogo?

## 7) Cenários Ao Vivo (Live Betting) e Momento
150. O Botafogo está pressionando muito nos últimos 10 minutos?
142. Qual time está com mais posse de bola ofensiva agora?
143. A odd do empate subiu muito após o gol?
144. O time da casa costuma levar a virada quando sai ganhando?
145. Vale a pena entrar em "Over Escanteios" dado o ritmo atual do jogo?
146. O goleiro visitante está fazendo muitas defesas difíceis?
147. Quantos chutes o Flamengo deu desde que o adversário foi expulso?
148. O time que está perdendo costuma marcar gols no final do 2º tempo?
149. A linha de gols asiáticos mudou como no intervalo?
150. Qual a probabilidade estatística desse 0x0 se manter até o final?

## 8) Escalações, Lesões e Notícias
160. O Palmeiras vai jogar com time titular ou reserva?
152. Quem são os desfalques do Flamengo para o jogo de hoje?
153. O artilheiro do time visitante está lesionado?
154. Qual a escalação provável do São Paulo?
155. O técnico do Grêmio costuma poupar jogadores na Copa do Brasil?
156. Quem é o substituto do goleiro titular do Santos?
157. O time vai jogar com três zagueiros hoje?
158. Impacto da ausência do Hulk nas odds do Atlético-MG.
159. O lateral titular foi convocado para a seleção?
160. O time joga melhor ou pior sem o seu camisa 10?

## 9) Consultoria e Estratégia (Tipster AI)
170. Com base nas estatísticas, qual a aposta mais segura de hoje?
162. Monte uma múltipla com odds totais de 3.0 para a rodada.
163. Existe alguma "zebra" com valor matemático claro nesta rodada?
164. Qual jogo tem a maior disparidade entre a odd e a probabilidade real?
165. Me dê 3 motivos para apostar na vitória do Bahia hoje.
166. O mercado de "Ambas Marcam" é bom para o clássico Gre-Nal?
167. Baseado no xG (Gols Esperados), o Vasco deveria ter ganhado o último jogo?
168. Estou pensando em apostar no Fortaleza, existe algum contra-indicativo estatístico?
169. Qual a melhor estratégia para jogos do Bragantino: gols ou escanteios?
170. Analise o confronto Cruzeiro x Vasco e me dê um palpite de placar exato.