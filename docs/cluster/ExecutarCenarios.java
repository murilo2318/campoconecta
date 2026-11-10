import ispd.arquivo.xml.IconicoXML;
import ispd.gui.JResultados;
import ispd.arquivo.SalvarResultadosHTML;
import ispd.motor.*;
import ispd.motor.filas.*;
import ispd.motor.filas.servidores.*;
import ispd.motor.metricas.*;
import java.awt.Color;
import java.io.*;
import java.nio.file.*;
import java.util.*;
import org.w3c.dom.Document;

/** Adapter de entrada/saída: não altera o motor nem o JAR do iSPD 2.0. */
public class ExecutarCenarios {
  public static void main(String[] args) throws Exception {
    Locale.setDefault(Locale.US);
    Path modelo = Path.of(args[0]), destino = Path.of(args[1]);
    Files.createDirectories(destino);
    Document doc = IconicoXML.ler(modelo.toFile());
    IconicoXML.validarModelo(doc);
    RedeDeFilas rede = IconicoXML.newRedeDeFilas(doc);
    int n = rede.getMaquinas().size();
    if (n != 2 && n != 4) throw new IllegalStateException("Workers inesperados: " + n);
    if (rede.getMestres().size() != 1) throw new IllegalStateException("É necessário um mestre");
    List<Tarefa> tarefas = new ArrayList<>();
    // Unidades do iSPD: entrada/retorno Mbit; computação MFlops; chegada segundos.
    // Construtor público permite retorno separado, ausente no formulário/XML do gerador.
    for (int i=0; i<500; i++) tarefas.add(new Tarefa(i,"user1","classificar_relato",rede.getMestres().get(0),0.016,0.008,136.0,0.0));
    ProgressoSimulacao progresso = new ProgressoSimulacao() {
      public void incProgresso(int x) {}
      public void print(String s, Color c) { System.out.print(s); }
    };
    Simulacao sim = new SimulacaoSequencial(progresso, rede, tarefas);
    sim.criarRoteamento(); sim.simular();
    Metricas metricas = sim.getMetricas();
    double t = metricas.getMetricasGlobais().getTempoSimulacao();
    long concluidas = tarefas.stream().filter(x -> x.getEstado()==Tarefa.CONCLUIDO).count();
    if(concluidas!=500) throw new IllegalStateException("Concluídas: " + concluidas);
    StringBuilder csv=new StringBuilder("recurso,tarefas_concluidas,mflops_processados,segundos_ocupado,uso_percentual\n");
    int soma=0;
    for (CS_Processamento w : rede.getMaquinas()) {
      long quantidade=tarefas.stream().filter(x->x.getLocalProcessamento()==w && x.getEstado()==Tarefa.CONCLUIDO).count();
      MetricasProcessamento m=w.getMetrica(); soma+=quantidade;
      csv.append(String.format(Locale.US,"%s_%d,%d,%.12f,%.12f,%.9f%n",w.getId(),w.getnumeroMaquina(),quantidade,m.getMFlopsProcessados(),m.getSegundosDeProcessamento(),100*m.getSegundosDeProcessamento()/t));
    }
    if(soma!=500)throw new IllegalStateException("Tarefas nos workers: "+soma);
    Files.writeString(destino.resolve("recursos.csv"),csv.toString());
    Files.writeString(destino.resolve("resultado.json"),String.format(Locale.US,"{\"simulador\":\"iSPD 2.0 oficial\",\"workers\":%d,\"tarefas\":500,\"concluidas\":%d,\"total_simulated_time_s\":%.15f,\"entrada_mbit\":0.016,\"saida_mbit\":0.008,\"mflops_tarefa\":136.0,\"chegada_s\":0.0,\"mestre_mflops_processados\":%.12f}%n",n,concluidas,t,rede.getMestres().get(0).getMetrica().getMFlopsProcessados()));
    System.out.printf(Locale.US,"%nWorkers=%d | Total Simulated Time=%.15f s | Completed=%d%n",n,t,concluidas);
    System.out.println(csv);
    // Exportador oficial, as mesmas métricas que a janela Results/Resources.
    SalvarResultadosHTML html=new SalvarResultadosHTML();
    html.setMetricasGlobais(metricas.getMetricasGlobais()); html.setMetricasTarefas(metricas);
    Object[][] tabela=new Object[n+1][4];
    for(int i=0;i<n;i++){CS_Processamento w=rede.getMaquinas().get(i);tabela[i]=new Object[]{w.getId()+"_"+w.getnumeroMaquina(),w.getProprietario(),w.getMetrica().getSegundosDeProcessamento(),0};}
    tabela[n]=new Object[]{"Mestre","user1",rede.getMestres().get(0).getMetrica().getSegundosDeProcessamento(),0};
    html.setTabela(tabela); html.setSatisfacao(new Object[0][0]); html.setCharts(new java.awt.image.BufferedImage[0]);
    html.gerarHTML(destino.toFile());
    if(args.length>2 && args[2].equals("--gui")) {
      JResultados janela=new JResultados((java.awt.Window)null,metricas,rede,tarefas,new ispd.arquivo.xml.ConfiguracaoISPD());
      janela.setTitle("iSPD — CampoConecta — "+n+" workers (retorno exato 0.008 Mbit)");
      janela.setModal(false); janela.setVisible(true);
    } else { System.exit(0); }
  }
}
