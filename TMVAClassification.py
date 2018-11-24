


<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
    "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
<head>
<meta name="robots" content="index,follow" />
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
<meta name="generator" content="0.11.1 (2b48ae40ea1b)" />
<meta http-equiv="X-UA-Compatible" content="IE=8" />
<link rel="icon" href="/source/default/img/icon.png" type="image/png" />
<link rel="stylesheet" type="text/css" media="all"
    title="Default" href="/source/default/style.css" />
<link rel="alternate stylesheet" type="text/css" media="all"
    title="Paper White" href="/source/default/print.css" />
<link rel="stylesheet" type="text/css" href="/source/default/print.css" media="print" />
<link rel="stylesheet" type="text/css" href="/source/default/jquery.tooltip.css" />

<link rel="search" href="/source/opensearch"
    type="application/opensearchdescription+xml"
    title="OpenGrok Search for current project(s)" />
<script type="text/javascript" src="/source/jquery-1.4.4.min.js"></script>
<script type="text/javascript" src="/source/jquery.tooltip-1.3.pack.js"></script>

<script type="text/javascript" src="/source/utils.js"></script>
<title>Cross Reference: /cern/root/tmva/test/TMVAClassification.py</title>
</head>
<body>
<script type="text/javascript">/* <![CDATA[ */
    document.hash = 'null';document.rev = '';document.link = '/source/xref/cern/root/tmva/test/TMVAClassification.py';document.annotate = false;
    document.domReady.push(function() {domReadyMast();});
    document.pageReady.push(function() { pageReadyMast();});
/* ]]> */</script>
<div id="page">
    <div id="whole_header">
        <form action="/source/search">
<div id="header">
<a href="/source/" class="cslogo">
    <span style="color: #5a2c00; letter-spacing: -2px;">{</span><span 
        style="color: #0f3368; vertical-align: middle;">Code</span>
    <span style="color: #222222; vertical-align: middle;">Search</span>
</a>
<span id="partner">
    <a href="http://www.metager.de"><span id="partner_metager"></span></a>
</span>



    <div id="pagetitle"><span id="filename"
                    >Cross Reference: TMVAClassification.py</span></div>
</div>
<div id="Masthead">
    <tt><a href="/source/xref/">xref</a>: /<a href="/source/xref/cern/">cern</a>/<a href="/source/xref/cern/root/">root</a>/<a href="/source/xref/cern/root/tmva/">tmva</a>/<a href="/source/xref/cern/root/tmva/test/">test</a>/<a href="/source/xref/cern/root/tmva/test/TMVAClassification.py">TMVAClassification.py</a></tt>
</div>
<div id="bar">
    <ul>
        <li><a href="/source/"><span id="home"></span>Home</a></li><li><a href="/source/history/cern/root/tmva/test/TMVAClassification.py"><span id="history"></span>History</a></li><li><a href="#" onclick="javascript:get_annotations(); return false;"
            ><span class="annotate"></span>Annotate</a></li><li><a href="#" onclick="javascript:lntoggle();return false;"
            title="Show or hide line numbers (might be slower if file has more than 10 000 lines)."><span id="line"></span>Line#</a></li><li><a
            href="#" onclick="javascript:lsttoggle();return false;"
            title="Show or hide symbol list."><span id="defbox"></span>Navigate</a></li><li><a href="/source/raw/cern/root/tmva/test/TMVAClassification.py"><span id="download"></span>Download</a></li><li><input type="text" id="search" name="q" class="q" />
            <input type="submit" value="Search" class="submit" /></li><li><input type="checkbox" name="path" value="/cern/root/tmva/test/" /> only in <b>TMVAClassification.py</b></li>
        
    </ul>
    <input type="hidden" name="project" value="cern" />
</div>
        </form>
    </div>
<div id="content">
<script type="text/javascript">/* <![CDATA[ */
document.pageReady.push(function() { pageReadyList();});
/* ]]> */</script>

<div id="src">
    <pre><script type="text/javascript">/* <![CDATA[ */
function get_sym_list(){return [["Variable","xv",[["DEFAULT_INFNAME",43],["DEFAULT_METHODS",46],["DEFAULT_OUTFNAME",42],["DEFAULT_TREEBKG",45],["DEFAULT_TREESIG",44]]],["Namespace","xn",[["TCut",115],["TFile",115],["TMVA",131],["TTree",115],["accounting",36],["command",37],["exit",35],["gApplication",115],["gROOT",115],["gSystem",115],["getopt",37],["line",37],["parser",37],["sys",35],["time",36]]],["Function","xf",[["main",63],["usage",49]]]];} /* ]]> */</script><a class="l" name="1" href="#1">1</a><span class="c">#!/<a href="/source/s?path=/usr/">usr</a>/<a href="/source/s?path=/usr/bin/">bin</a>/<a href="/source/s?path=/usr/bin/env">env</a> python</span>
<a class="l" name="2" href="#2">2</a><span class="c"># @(#)<a href="/source/s?path=root/">root</a>/<a href="/source/s?path=root/tmva">tmva</a> $Id$</span>
<a class="l" name="3" href="#3">3</a><span class="c"># ------------------------------------------------------------------------------ #</span>
<a class="l" name="4" href="#4">4</a><span class="c"># Project      : TMVA - a Root-integrated toolkit for multivariate data analysis #</span>
<a class="l" name="5" href="#5">5</a><span class="c"># Package      : TMVA                                                            #</span>
<a class="l" name="6" href="#6">6</a><span class="c"># Python script: <a href="/source/s?path=TMVAClassification.py&amp;project=cern">TMVAClassification.py</a>                                           #</span>
<a class="l" name="7" href="#7">7</a><span class="c">#                                                                                #</span>
<a class="l" name="8" href="#8">8</a><span class="c"># This python script provides examples for the training and testing of all the   #</span>
<a class="l" name="9" href="#9">9</a><span class="c"># TMVA classifiers through PyROOT.                                               #</span>
<a class="hl" name="10" href="#10">10</a><span class="c">#                                                                                #</span>
<a class="l" name="11" href="#11">11</a><span class="c"># The Application works similarly, please see:                                   #</span>
<a class="l" name="12" href="#12">12</a><span class="c">#    <a href="/source/s?path=TMVA/">TMVA</a>/<a href="/source/s?path=TMVA/macros/">macros</a>/<a href="/source/s?path=TMVA/macros/TMVAClassificationApplication.C">TMVAClassificationApplication.C</a>                                 #</span>
<a class="l" name="13" href="#13">13</a><span class="c"># For regression, see:                                                           #</span>
<a class="l" name="14" href="#14">14</a><span class="c">#    <a href="/source/s?path=TMVA/">TMVA</a>/<a href="/source/s?path=TMVA/macros/">macros</a>/<a href="/source/s?path=TMVA/macros/TMVARegression.C">TMVARegression.C</a>                                                #</span>
<a class="l" name="15" href="#15">15</a><span class="c">#    <a href="/source/s?path=TMVA/">TMVA</a>/<a href="/source/s?path=TMVA/macros/">macros</a>/<a href="/source/s?path=TMVA/macros/TMVARegressionpplication.C">TMVARegressionpplication.C</a>                                      #</span>
<a class="l" name="16" href="#16">16</a><span class="c"># and translate to python as done here.                                          #</span>
<a class="l" name="17" href="#17">17</a><span class="c">#                                                                                #</span>
<a class="l" name="18" href="#18">18</a><span class="c"># As input data is used a toy-MC sample consisting of four Gaussian-distributed  #</span>
<a class="l" name="19" href="#19">19</a><span class="c"># and linearly correlated input variables.                                       #</span>
<a class="hl" name="20" href="#20">20</a><span class="c">#                                                                                #</span>
<a class="l" name="21" href="#21">21</a><span class="c"># The methods to be used can be switched on and off via the prompt command, for  #</span>
<a class="l" name="22" href="#22">22</a><span class="c"># example:                                                                       #</span>
<a class="l" name="23" href="#23">23</a><span class="c">#                                                                                #</span>
<a class="l" name="24" href="#24">24</a><span class="c">#    python <a href="/source/s?path=TMVAClassification.py&amp;project=cern">TMVAClassification.py</a> --methods Fisher,Likelihood                    #</span>
<a class="l" name="25" href="#25">25</a><span class="c">#                                                                                #</span>
<a class="l" name="26" href="#26">26</a><span class="c"># The output file "TMVA.root" can be analysed with the use of dedicated          #</span>
<a class="l" name="27" href="#27">27</a><span class="c"># macros (simply say: root -l &lt;../<a href="/source/s?path=/macros/">macros</a>/<a href="/source/s?path=/macros/macro.C">macro.C</a>&gt;), which can be conveniently    #</span>
<a class="l" name="28" href="#28">28</a><span class="c"># invoked through a GUI that will appear at the end of the run of this macro.    #</span>
<a class="l" name="29" href="#29">29</a><span class="c">#                                                                                #</span>
<a class="hl" name="30" href="#30">30</a><span class="c"># for help type "python <a href="/source/s?path=TMVAClassification.py&amp;project=cern">TMVAClassification.py</a> --help"                            #</span>
<a class="l" name="31" href="#31">31</a><span class="c"># ------------------------------------------------------------------------------ #</span>
<a class="l" name="32" href="#32">32</a>
<a class="l" name="33" href="#33">33</a><span class="c"># --------------------------------------------</span>
<a class="l" name="34" href="#34">34</a><span class="c"># Standard python import</span>
<a class="l" name="35" href="#35">35</a><b>import</b> <a class="xn" name="sys"/><a href="/source/s?refs=sys&amp;project=cern" class="xn">sys</a>    <span class="c"># exit</span>
<a class="l" name="36" href="#36">36</a><b>import</b> <a class="xn" name="time"/><a href="/source/s?refs=time&amp;project=cern" class="xn">time</a>   <span class="c"># time accounting</span>
<a class="l" name="37" href="#37">37</a><b>import</b> <a class="xn" name="getopt"/><a href="/source/s?refs=getopt&amp;project=cern" class="xn">getopt</a> <span class="c"># command line parser</span>
<a class="l" name="38" href="#38">38</a>
<a class="l" name="39" href="#39">39</a><span class="c"># --------------------------------------------</span>
<a class="hl" name="40" href="#40">40</a>
<a class="l" name="41" href="#41">41</a><span class="c"># Default settings for command line arguments</span>
<a class="l" name="42" href="#42">42</a><a class="xv" name="DEFAULT_OUTFNAME"/><a href="/source/s?refs=DEFAULT_OUTFNAME&amp;project=cern" class="xv">DEFAULT_OUTFNAME</a> = <span class="s">"TMVA.root"</span>
<a class="l" name="43" href="#43">43</a><a class="xv" name="DEFAULT_INFNAME"/><a href="/source/s?refs=DEFAULT_INFNAME&amp;project=cern" class="xv">DEFAULT_INFNAME</a>  = <span class="s">"tmva_class_example.root"</span>
<a class="l" name="44" href="#44">44</a><a class="xv" name="DEFAULT_TREESIG"/><a href="/source/s?refs=DEFAULT_TREESIG&amp;project=cern" class="xv">DEFAULT_TREESIG</a>  = <span class="s">"TreeS"</span>
<a class="l" name="45" href="#45">45</a><a class="xv" name="DEFAULT_TREEBKG"/><a href="/source/s?refs=DEFAULT_TREEBKG&amp;project=cern" class="xv">DEFAULT_TREEBKG</a>  = <span class="s">"TreeB"</span>
<a class="l" name="46" href="#46">46</a><a class="xv" name="DEFAULT_METHODS"/><a href="/source/s?refs=DEFAULT_METHODS&amp;project=cern" class="xv">DEFAULT_METHODS</a>  = <span class="s">"Cuts,CutsD,CutsPCA,CutsGA,CutsSA,Likelihood,LikelihoodD,LikelihoodPCA,LikelihoodKDE,LikelihoodMIX,PDERS,PDERSD,PDERSPCA,PDEFoam,PDEFoamBoost,KNN,LD,Fisher,FisherG,BoostedFisher,HMatrix,FDA_GA,FDA_SA,FDA_MC,FDA_MT,FDA_GAMT,FDA_MCMT,MLP,MLPBFGS,MLPBNN,CFMlpANN,TMlpANN,SVM,BDT,BDTD,BDTG,BDTB,RuleFit"</span>
<a class="l" name="47" href="#47">47</a>
<a class="l" name="48" href="#48">48</a><span class="c"># Print usage help</span>
<a class="l" name="49" href="#49">49</a><b>def</b> <a class="xf" name="usage"/><a href="/source/s?refs=usage&amp;project=cern" class="xf">usage</a>():
<a class="hl" name="50" href="#50">50</a>    <b>print</b> <span class="s">" "</span>
<a class="l" name="51" href="#51">51</a>    <b>print</b> <span class="s">"Usage: python %s [options]"</span> % <a class="d" href="#sys">sys</a>.<a href="/source/s?defs=argv&amp;project=cern">argv</a>[<span class="n">0</span>]
<a class="l" name="52" href="#52">52</a>    <b>print</b> <span class="s">"  -m | --methods    : gives methods to be run (default: all methods)"</span>
<a class="l" name="53" href="#53">53</a>    <b>print</b> <span class="s">"  -i | --inputfile  : name of input ROOT file (default: '%s')"</span> % <a class="d" href="#DEFAULT_INFNAME">DEFAULT_INFNAME</a>
<a class="l" name="54" href="#54">54</a>    <b>print</b> <span class="s">"  -o | --outputfile : name of output ROOT file containing results (default: '%s')"</span> % <a class="d" href="#DEFAULT_OUTFNAME">DEFAULT_OUTFNAME</a>
<a class="l" name="55" href="#55">55</a>    <b>print</b> <span class="s">"  -t | --inputtrees : input ROOT Trees for signal and background (default: '%s %s')"</span> \
<a class="l" name="56" href="#56">56</a>          % (<a class="d" href="#DEFAULT_TREESIG">DEFAULT_TREESIG</a>, <a class="d" href="#DEFAULT_TREEBKG">DEFAULT_TREEBKG</a>)
<a class="l" name="57" href="#57">57</a>    <b>print</b> <span class="s">"  -v | --verbose"</span>
<a class="l" name="58" href="#58">58</a>    <b>print</b> <span class="s">"  -? | --usage      : print this help message"</span>
<a class="l" name="59" href="#59">59</a>    <b>print</b> <span class="s">"  -h | --help       : print this help message"</span>
<a class="hl" name="60" href="#60">60</a>    <b>print</b> <span class="s">" "</span>
<a class="l" name="61" href="#61">61</a>
<a class="l" name="62" href="#62">62</a><span class="c"># Main routine</span>
<a class="l" name="63" href="#63">63</a><b>def</b> <a class="xf" name="main"/><a href="/source/s?refs=main&amp;project=cern" class="xf">main</a>():
<a class="l" name="64" href="#64">64</a>
<a class="l" name="65" href="#65">65</a>    <b>try</b>:
<a class="l" name="66" href="#66">66</a>        <span class="c"># retrive command line options</span>
<a class="l" name="67" href="#67">67</a>        <a href="/source/s?defs=shortopts&amp;project=cern">shortopts</a>  = <span class="s">"m:i:t:o:vh?"</span>
<a class="l" name="68" href="#68">68</a>        <a href="/source/s?defs=longopts&amp;project=cern">longopts</a>   = [<span class="s">"methods="</span>, <span class="s">"inputfile="</span>, <span class="s">"inputtrees="</span>, <span class="s">"outputfile="</span>, <span class="s">"verbose"</span>, <span class="s">"help"</span>, <span class="s">"usage"</span>]
<a class="l" name="69" href="#69">69</a>        <a href="/source/s?defs=opts&amp;project=cern">opts</a>, <a href="/source/s?defs=args&amp;project=cern">args</a> = <a class="d" href="#getopt">getopt</a>.<a class="d" href="#getopt">getopt</a>( <a class="d" href="#sys">sys</a>.<a href="/source/s?defs=argv&amp;project=cern">argv</a>[<span class="n">1</span>:], <a href="/source/s?defs=shortopts&amp;project=cern">shortopts</a>, <a href="/source/s?defs=longopts&amp;project=cern">longopts</a> )
<a class="hl" name="70" href="#70">70</a>
<a class="l" name="71" href="#71">71</a>    <b>except</b> <a class="d" href="#getopt">getopt</a>.<a href="/source/s?defs=GetoptError&amp;project=cern">GetoptError</a>:
<a class="l" name="72" href="#72">72</a>        <span class="c"># print help information and exit:</span>
<a class="l" name="73" href="#73">73</a>        <b>print</b> <span class="s">"ERROR: unknown options in argument %s"</span> % <a class="d" href="#sys">sys</a>.<a href="/source/s?defs=argv&amp;project=cern">argv</a>[<span class="n">1</span>:]
<a class="l" name="74" href="#74">74</a>        <a class="d" href="#usage">usage</a>()
<a class="l" name="75" href="#75">75</a>        <a class="d" href="#sys">sys</a>.<a class="d" href="#exit">exit</a>(<span class="n">1</span>)
<a class="l" name="76" href="#76">76</a>
<a class="l" name="77" href="#77">77</a>    <a href="/source/s?defs=infname&amp;project=cern">infname</a>     = <a class="d" href="#DEFAULT_INFNAME">DEFAULT_INFNAME</a>
<a class="l" name="78" href="#78">78</a>    <a href="/source/s?defs=treeNameSig&amp;project=cern">treeNameSig</a> = <a class="d" href="#DEFAULT_TREESIG">DEFAULT_TREESIG</a>
<a class="l" name="79" href="#79">79</a>    <a href="/source/s?defs=treeNameBkg&amp;project=cern">treeNameBkg</a> = <a class="d" href="#DEFAULT_TREEBKG">DEFAULT_TREEBKG</a>
<a class="hl" name="80" href="#80">80</a>    <a href="/source/s?defs=outfname&amp;project=cern">outfname</a>    = <a class="d" href="#DEFAULT_OUTFNAME">DEFAULT_OUTFNAME</a>
<a class="l" name="81" href="#81">81</a>    <a href="/source/s?defs=methods&amp;project=cern">methods</a>     = <a class="d" href="#DEFAULT_METHODS">DEFAULT_METHODS</a>
<a class="l" name="82" href="#82">82</a>    <a href="/source/s?defs=verbose&amp;project=cern">verbose</a>     = <a href="/source/s?defs=False&amp;project=cern">False</a>
<a class="l" name="83" href="#83">83</a>    <b>for</b> o, a <b>in</b> <a href="/source/s?defs=opts&amp;project=cern">opts</a>:
<a class="l" name="84" href="#84">84</a>        <b>if</b> o <b>in</b> (<span class="s">"-?"</span>, <span class="s">"-h"</span>, <span class="s">"--help"</span>, <span class="s">"--usage"</span>):
<a class="l" name="85" href="#85">85</a>            <a class="d" href="#usage">usage</a>()
<a class="l" name="86" href="#86">86</a>            <a class="d" href="#sys">sys</a>.<a class="d" href="#exit">exit</a>(<span class="n">0</span>)
<a class="l" name="87" href="#87">87</a>        <b>elif</b> o <b>in</b> (<span class="s">"-m"</span>, <span class="s">"--methods"</span>):
<a class="l" name="88" href="#88">88</a>            <a href="/source/s?defs=methods&amp;project=cern">methods</a> = a
<a class="l" name="89" href="#89">89</a>        <b>elif</b> o <b>in</b> (<span class="s">"-i"</span>, <span class="s">"--inputfile"</span>):
<a class="hl" name="90" href="#90">90</a>            <a href="/source/s?defs=infname&amp;project=cern">infname</a> = a
<a class="l" name="91" href="#91">91</a>        <b>elif</b> o <b>in</b> (<span class="s">"-o"</span>, <span class="s">"--outputfile"</span>):
<a class="l" name="92" href="#92">92</a>            <a href="/source/s?defs=outfname&amp;project=cern">outfname</a> = a
<a class="l" name="93" href="#93">93</a>        <b>elif</b> o <b>in</b> (<span class="s">"-t"</span>, <span class="s">"--inputtrees"</span>):
<a class="l" name="94" href="#94">94</a>            a.<a href="/source/s?defs=strip&amp;project=cern">strip</a>()
<a class="l" name="95" href="#95">95</a>            <a href="/source/s?defs=trees&amp;project=cern">trees</a> = a.<a href="/source/s?defs=rsplit&amp;project=cern">rsplit</a>( <span class="s">' '</span> )
<a class="l" name="96" href="#96">96</a>            <a href="/source/s?defs=trees&amp;project=cern">trees</a>.<a href="/source/s?defs=sort&amp;project=cern">sort</a>()
<a class="l" name="97" href="#97">97</a>            <a href="/source/s?defs=trees&amp;project=cern">trees</a>.<a href="/source/s?defs=reverse&amp;project=cern">reverse</a>()
<a class="l" name="98" href="#98">98</a>            <b>if</b> <a href="/source/s?defs=len&amp;project=cern">len</a>(<a href="/source/s?defs=trees&amp;project=cern">trees</a>)-<a href="/source/s?defs=trees&amp;project=cern">trees</a>.<a href="/source/s?defs=count&amp;project=cern">count</a>(<span class="s">''</span>) != <span class="n">2</span>:
<a class="l" name="99" href="#99">99</a>                <b>print</b> <span class="s">"ERROR: need to give two trees (each one for signal and background)"</span>
<a class="hl" name="100" href="#100">100</a>                <b>print</b> <a href="/source/s?defs=trees&amp;project=cern">trees</a>
<a class="l" name="101" href="#101">101</a>                <a class="d" href="#sys">sys</a>.<a class="d" href="#exit">exit</a>(<span class="n">1</span>)
<a class="l" name="102" href="#102">102</a>            <a href="/source/s?defs=treeNameSig&amp;project=cern">treeNameSig</a> = <a href="/source/s?defs=trees&amp;project=cern">trees</a>[<span class="n">0</span>]
<a class="l" name="103" href="#103">103</a>            <a href="/source/s?defs=treeNameBkg&amp;project=cern">treeNameBkg</a> = <a href="/source/s?defs=trees&amp;project=cern">trees</a>[<span class="n">1</span>]
<a class="l" name="104" href="#104">104</a>        <b>elif</b> o <b>in</b> (<span class="s">"-v"</span>, <span class="s">"--verbose"</span>):
<a class="l" name="105" href="#105">105</a>            <a href="/source/s?defs=verbose&amp;project=cern">verbose</a> = <a href="/source/s?defs=True&amp;project=cern">True</a>
<a class="l" name="106" href="#106">106</a>
<a class="l" name="107" href="#107">107</a>    <span class="c"># Print methods</span>
<a class="l" name="108" href="#108">108</a>    <a href="/source/s?defs=mlist&amp;project=cern">mlist</a> = <a href="/source/s?defs=methods&amp;project=cern">methods</a>.<a href="/source/s?defs=replace&amp;project=cern">replace</a>(<span class="s">' '</span>,<span class="s">','</span>).<a href="/source/s?defs=split&amp;project=cern">split</a>(<span class="s">','</span>)
<a class="l" name="109" href="#109">109</a>    <b>print</b> <span class="s">"=== TMVAClassification: use method(s)..."</span>
<a class="hl" name="110" href="#110">110</a>    <b>for</b> m <b>in</b> <a href="/source/s?defs=mlist&amp;project=cern">mlist</a>:
<a class="l" name="111" href="#111">111</a>        <b>if</b> m.<a href="/source/s?defs=strip&amp;project=cern">strip</a>() != <span class="s">''</span>:
<a class="l" name="112" href="#112">112</a>            <b>print</b> <span class="s">"=== - &lt;%s&gt;"</span> % m.<a href="/source/s?defs=strip&amp;project=cern">strip</a>()
<a class="l" name="113" href="#113">113</a>
<a class="l" name="114" href="#114">114</a>    <span class="c"># Import ROOT classes</span>
<a class="l" name="115" href="#115">115</a>    <b>from</b> <a href="/source/s?defs=ROOT&amp;project=cern">ROOT</a> <b>import</b> <a class="xn" name="gSystem"/><a href="/source/s?refs=gSystem&amp;project=cern" class="xn">gSystem</a>, <a class="xn" name="gROOT"/><a href="/source/s?refs=gROOT&amp;project=cern" class="xn">gROOT</a>, <a class="xn" name="gApplication"/><a href="/source/s?refs=gApplication&amp;project=cern" class="xn">gApplication</a>, <a class="xn" name="TFile"/><a href="/source/s?refs=TFile&amp;project=cern" class="xn">TFile</a>, <a class="xn" name="TTree"/><a href="/source/s?refs=TTree&amp;project=cern" class="xn">TTree</a>, <a class="xn" name="TCut"/><a href="/source/s?refs=TCut&amp;project=cern" class="xn">TCut</a>
<a class="l" name="116" href="#116">116</a>
<a class="l" name="117" href="#117">117</a>    <span class="c"># check ROOT version, give alarm if 5.18</span>
<a class="l" name="118" href="#118">118</a>    <b>if</b> <a class="d" href="#gROOT">gROOT</a>.<a href="/source/s?defs=GetVersionCode&amp;project=cern">GetVersionCode</a>() &gt;= <span class="n">332288</span> <b>and</b> <a class="d" href="#gROOT">gROOT</a>.<a href="/source/s?defs=GetVersionCode&amp;project=cern">GetVersionCode</a>() &lt; <span class="n">332544</span>:
<a class="l" name="119" href="#119">119</a>        <b>print</b> <span class="s">"*** You are running ROOT version 5.18, which has problems in PyROOT such that TMVA"</span>
<a class="hl" name="120" href="#120">120</a>        <b>print</b> <span class="s">"*** does not run properly (function calls with enums in the argument are ignored)."</span>
<a class="l" name="121" href="#121">121</a>        <b>print</b> <span class="s">"*** Solution: either use CINT or a C++ compiled version (see <a href="/source/s?path=TMVA/">TMVA</a>/<a href="/source/s?path=TMVA/macros">macros</a> or <a href="/source/s?path=TMVA/">TMVA</a>/<a href="/source/s?path=TMVA/examples">examples</a>),"</span>
<a class="l" name="122" href="#122">122</a>        <b>print</b> <span class="s">"*** or use another ROOT version (e.g., ROOT 5.19)."</span>
<a class="l" name="123" href="#123">123</a>        <a class="d" href="#sys">sys</a>.<a class="d" href="#exit">exit</a>(<span class="n">1</span>)
<a class="l" name="124" href="#124">124</a>
<a class="l" name="125" href="#125">125</a>    <span class="c"># Logon not automatically loaded through PyROOT (logon loads TMVA library) load also GUI</span>
<a class="l" name="126" href="#126">126</a>    <a class="d" href="#gROOT">gROOT</a>.<a href="/source/s?defs=SetMacroPath&amp;project=cern">SetMacroPath</a>( <span class="s">"./"</span> )
<a class="l" name="127" href="#127">127</a>    <a class="d" href="#gROOT">gROOT</a>.<a href="/source/s?defs=Macro&amp;project=cern">Macro</a>       ( <span class="s">"./TMVAlogon.C"</span> )
<a class="l" name="128" href="#128">128</a>    <a class="d" href="#gROOT">gROOT</a>.<a href="/source/s?defs=LoadMacro&amp;project=cern">LoadMacro</a>   ( <span class="s">"./TMVAGui.C"</span> )
<a class="l" name="129" href="#129">129</a>
<a class="hl" name="130" href="#130">130</a>    <span class="c"># Import TMVA classes from ROOT</span>
<a class="l" name="131" href="#131">131</a>    <b>from</b> <a href="/source/s?defs=ROOT&amp;project=cern">ROOT</a> <b>import</b> <a class="xn" name="TMVA"/><a href="/source/s?refs=TMVA&amp;project=cern" class="xn">TMVA</a>
<a class="l" name="132" href="#132">132</a>
<a class="l" name="133" href="#133">133</a>    <span class="c"># Output file</span>
<a class="l" name="134" href="#134">134</a>    <a href="/source/s?defs=outputFile&amp;project=cern">outputFile</a> = <a class="d" href="#TFile">TFile</a>( <a href="/source/s?defs=outfname&amp;project=cern">outfname</a>, <span class="s">'RECREATE'</span> )
<a class="l" name="135" href="#135">135</a>
<a class="l" name="136" href="#136">136</a>    <span class="c"># Create instance of TMVA factory (see <a href="/source/s?path=TMVA/">TMVA</a>/<a href="/source/s?path=TMVA/macros/">macros</a>/<a href="/source/s?path=TMVA/macros/TMVAClassification.C">TMVAClassification.C</a> for more factory options)</span>
<a class="l" name="137" href="#137">137</a>    <span class="c"># All TMVA output can be suppressed by removing the "!" (not) in</span>
<a class="l" name="138" href="#138">138</a>    <span class="c"># front of the "Silent" argument in the option string</span>
<a class="l" name="139" href="#139">139</a>    <a href="/source/s?defs=factory&amp;project=cern">factory</a> = <a class="d" href="#TMVA">TMVA</a>.<a href="/source/s?defs=Factory&amp;project=cern">Factory</a>( <span class="s">"TMVAClassification"</span>, <a href="/source/s?defs=outputFile&amp;project=cern">outputFile</a>,
<a class="hl" name="140" href="#140">140</a>                            <span class="s">"!V:!Silent:Color:DrawProgressBar:Transformations=I;D;P;G,D:AnalysisType=Classification"</span> )
<a class="l" name="141" href="#141">141</a>
<a class="l" name="142" href="#142">142</a>    <span class="c"># Set verbosity</span>
<a class="l" name="143" href="#143">143</a>    <a href="/source/s?defs=factory&amp;project=cern">factory</a>.<a href="/source/s?defs=SetVerbose&amp;project=cern">SetVerbose</a>( <a href="/source/s?defs=verbose&amp;project=cern">verbose</a> )
<a class="l" name="144" href="#144">144</a>
<a class="l" name="145" href="#145">145</a>    <span class="c"># If you wish to modify default settings</span>
<a class="l" name="146" href="#146">146</a>    <span class="c"># (please check "<a href="/source/s?path=src/">src</a>/<a href="/source/s?path=src/Config.h">Config.h</a>" to see all available global options)</span>
<a class="l" name="147" href="#147">147</a>    <span class="c">#    gConfig().GetVariablePlotting()).fTimesRMS = 8.0</span>
<a class="l" name="148" href="#148">148</a>    <span class="c">#    gConfig().GetIONames()).fWeightFileDir = "myWeightDirectory"</span>
<a class="l" name="149" href="#149">149</a>
<a class="hl" name="150" href="#150">150</a>    <span class="c"># Define the input variables that shall be used for the classifier training</span>
<a class="l" name="151" href="#151">151</a>    <span class="c"># note that you may also use variable expressions, such as: "3*<a href="/source/s?path=var1/">var1</a>/<a href="/source/s?path=var1/var2">var2</a>*abs(var3)"</span>
<a class="l" name="152" href="#152">152</a>    <span class="c"># [all types of expressions that can also be parsed by TTree::Draw( "expression" )]</span>
<a class="l" name="153" href="#153">153</a>    <a href="/source/s?defs=factory&amp;project=cern">factory</a>.<a href="/source/s?defs=AddVariable&amp;project=cern">AddVariable</a>( <span class="s">"myvar1 := var1+var2"</span>, <span class="s">'F'</span> )
<a class="l" name="154" href="#154">154</a>    <a href="/source/s?defs=factory&amp;project=cern">factory</a>.<a href="/source/s?defs=AddVariable&amp;project=cern">AddVariable</a>( <span class="s">"myvar2 := var1-var2"</span>, <span class="s">"Expression 2"</span>, <span class="s">""</span>, <span class="s">'F'</span> )
<a class="l" name="155" href="#155">155</a>    <a href="/source/s?defs=factory&amp;project=cern">factory</a>.<a href="/source/s?defs=AddVariable&amp;project=cern">AddVariable</a>( <span class="s">"var3"</span>,                <span class="s">"Variable 3"</span>, <span class="s">"units"</span>, <span class="s">'F'</span> )
<a class="l" name="156" href="#156">156</a>    <a href="/source/s?defs=factory&amp;project=cern">factory</a>.<a href="/source/s?defs=AddVariable&amp;project=cern">AddVariable</a>( <span class="s">"var4"</span>,                <span class="s">"Variable 4"</span>, <span class="s">"units"</span>, <span class="s">'F'</span> )
<a class="l" name="157" href="#157">157</a>
<a class="l" name="158" href="#158">158</a>    <span class="c"># You can add so-called "Spectator variables", which are not used in the MVA training,</span>
<a class="l" name="159" href="#159">159</a>    <span class="c"># but will appear in the final "TestTree" produced by TMVA. This TestTree will contain the</span>
<a class="hl" name="160" href="#160">160</a>    <span class="c"># input variables, the response values of all trained MVAs, and the spectator variables</span>
<a class="l" name="161" href="#161">161</a>    <a href="/source/s?defs=factory&amp;project=cern">factory</a>.<a href="/source/s?defs=AddSpectator&amp;project=cern">AddSpectator</a>( <span class="s">"spec1:=var1*2"</span>,  <span class="s">"Spectator 1"</span>, <span class="s">"units"</span>, <span class="s">'F'</span> )
<a class="l" name="162" href="#162">162</a>    <a href="/source/s?defs=factory&amp;project=cern">factory</a>.<a href="/source/s?defs=AddSpectator&amp;project=cern">AddSpectator</a>( <span class="s">"spec2:=var1*3"</span>,  <span class="s">"Spectator 2"</span>, <span class="s">"units"</span>, <span class="s">'F'</span> )
<a class="l" name="163" href="#163">163</a>
<a class="l" name="164" href="#164">164</a>    <span class="c"># Read input data</span>
<a class="l" name="165" href="#165">165</a>    <b>if</b> <a class="d" href="#gSystem">gSystem</a>.<a href="/source/s?defs=AccessPathName&amp;project=cern">AccessPathName</a>( <a href="/source/s?defs=infname&amp;project=cern">infname</a> ) != <span class="n">0</span>: <a class="d" href="#gSystem">gSystem</a>.<a href="/source/s?defs=Exec&amp;project=cern">Exec</a>( <span class="s">"wget <a href="http://root.cern.ch/files/">http://root.cern.ch/files/</a>"</span> + <a href="/source/s?defs=infname&amp;project=cern">infname</a> )
<a class="l" name="166" href="#166">166</a>
<a class="l" name="167" href="#167">167</a>    <a href="/source/s?defs=input&amp;project=cern">input</a> = <a class="d" href="#TFile">TFile</a>.<a href="/source/s?defs=Open&amp;project=cern">Open</a>( <a href="/source/s?defs=infname&amp;project=cern">infname</a> )
<a class="l" name="168" href="#168">168</a>
<a class="l" name="169" href="#169">169</a>    <span class="c"># Get the signal and background trees for training</span>
<a class="hl" name="170" href="#170">170</a>    <a href="/source/s?defs=signal&amp;project=cern">signal</a>      = <a href="/source/s?defs=input&amp;project=cern">input</a>.<a href="/source/s?defs=Get&amp;project=cern">Get</a>( <a href="/source/s?defs=treeNameSig&amp;project=cern">treeNameSig</a> )
<a class="l" name="171" href="#171">171</a>    <a href="/source/s?defs=background&amp;project=cern">background</a>  = <a href="/source/s?defs=input&amp;project=cern">input</a>.<a href="/source/s?defs=Get&amp;project=cern">Get</a>( <a href="/source/s?defs=treeNameBkg&amp;project=cern">treeNameBkg</a> )
<a class="l" name="172" href="#172">172</a>
<a class="l" name="173" href="#173">173</a>    <span class="c"># Global event weights (see below for setting event-wise weights)</span>
<a class="l" name="174" href="#174">174</a>    <a href="/source/s?defs=signalWeight&amp;project=cern">signalWeight</a>     = <span class="n">1.0</span>
<a class="l" name="175" href="#175">175</a>    <a href="/source/s?defs=backgroundWeight&amp;project=cern">backgroundWeight</a> = <span class="n">1.0</span>
<a class="l" name="176" href="#176">176</a>
<a class="l" name="177" href="#177">177</a>    <span class="c"># ====== register trees ====================================================</span>
<a class="l" name="178" href="#178">178</a>    <span class="c">#</span>
<a class="l" name="179" href="#179">179</a>    <span class="c"># the following method is the prefered one:</span>
<a class="hl" name="180" href="#180">180</a>    <span class="c"># you can add an arbitrary number of signal or background trees</span>
<a class="l" name="181" href="#181">181</a>    <a href="/source/s?defs=factory&amp;project=cern">factory</a>.<a href="/source/s?defs=AddSignalTree&amp;project=cern">AddSignalTree</a>    ( <a href="/source/s?defs=signal&amp;project=cern">signal</a>,     <a href="/source/s?defs=signalWeight&amp;project=cern">signalWeight</a>     )
<a class="l" name="182" href="#182">182</a>    <a href="/source/s?defs=factory&amp;project=cern">factory</a>.<a href="/source/s?defs=AddBackgroundTree&amp;project=cern">AddBackgroundTree</a>( <a href="/source/s?defs=background&amp;project=cern">background</a>, <a href="/source/s?defs=backgroundWeight&amp;project=cern">backgroundWeight</a> )
<a class="l" name="183" href="#183">183</a>
<a class="l" name="184" href="#184">184</a>    <span class="c"># To give different trees for training and testing, do as follows:</span>
<a class="l" name="185" href="#185">185</a>    <span class="c">#    factory.AddSignalTree( signalTrainingTree, signalTrainWeight, "Training" )</span>
<a class="l" name="186" href="#186">186</a>    <span class="c">#    factory.AddSignalTree( signalTestTree,     signalTestWeight,  "Test" )</span>
<a class="l" name="187" href="#187">187</a>
<a class="l" name="188" href="#188">188</a>    <span class="c"># Use the following code instead of the above two or four lines to add signal and background</span>
<a class="l" name="189" href="#189">189</a>    <span class="c"># training and test events "by hand"</span>
<a class="hl" name="190" href="#190">190</a>    <span class="c"># NOTE that in this case one should not give expressions (such as "var1+var2") in the input</span>
<a class="l" name="191" href="#191">191</a>    <span class="c">#      variable definition, but simply compute the expression before adding the event</span>
<a class="l" name="192" href="#192">192</a>    <span class="c">#</span>
<a class="l" name="193" href="#193">193</a>    <span class="c">#    # --- begin ----------------------------------------------------------</span>
<a class="l" name="194" href="#194">194</a>    <span class="c">#</span>
<a class="l" name="195" href="#195">195</a>    <span class="c"># ... *** please lookup code in <a href="/source/s?path=TMVA/">TMVA</a>/<a href="/source/s?path=TMVA/macros/">macros</a>/<a href="/source/s?path=TMVA/macros/TMVAClassification.C">TMVAClassification.C</a> ***</span>
<a class="l" name="196" href="#196">196</a>    <span class="c">#</span>
<a class="l" name="197" href="#197">197</a>    <span class="c">#    # --- end ------------------------------------------------------------</span>
<a class="l" name="198" href="#198">198</a>    <span class="c">#</span>
<a class="l" name="199" href="#199">199</a>    <span class="c"># ====== end of register trees ==============================================</span>
<a class="hl" name="200" href="#200">200</a>
<a class="l" name="201" href="#201">201</a>    <span class="c"># Set individual event weights (the variables must exist in the original TTree)</span>
<a class="l" name="202" href="#202">202</a>    <span class="c">#    for signal    : factory.SetSignalWeightExpression    ("weight1*weight2");</span>
<a class="l" name="203" href="#203">203</a>    <span class="c">#    for background: factory.SetBackgroundWeightExpression("weight1*weight2");</span>
<a class="l" name="204" href="#204">204</a>    <a href="/source/s?defs=factory&amp;project=cern">factory</a>.<a href="/source/s?defs=SetBackgroundWeightExpression&amp;project=cern">SetBackgroundWeightExpression</a>( <span class="s">"weight"</span> )
<a class="l" name="205" href="#205">205</a>
<a class="l" name="206" href="#206">206</a>    <span class="c"># Apply additional cuts on the signal and background sample.</span>
<a class="l" name="207" href="#207">207</a>    <span class="c"># example for cut: mycut = TCut( "abs(var1)&lt;0.5 &amp;&amp; abs(var2-0.5)&lt;1" )</span>
<a class="l" name="208" href="#208">208</a>    <a href="/source/s?defs=mycutSig&amp;project=cern">mycutSig</a> = <a class="d" href="#TCut">TCut</a>( <span class="s">""</span> )
<a class="l" name="209" href="#209">209</a>    <a href="/source/s?defs=mycutBkg&amp;project=cern">mycutBkg</a> = <a class="d" href="#TCut">TCut</a>( <span class="s">""</span> )
<a class="hl" name="210" href="#210">210</a>
<a class="l" name="211" href="#211">211</a>    <span class="c"># Here, the relevant variables are copied over in new, slim trees that are</span>
<a class="l" name="212" href="#212">212</a>    <span class="c"># used for TMVA training and testing</span>
<a class="l" name="213" href="#213">213</a>    <span class="c"># "SplitMode=Random" means that the input events are randomly shuffled before</span>
<a class="l" name="214" href="#214">214</a>    <span class="c"># splitting them into training and test samples</span>
<a class="l" name="215" href="#215">215</a>    <a href="/source/s?defs=factory&amp;project=cern">factory</a>.<a href="/source/s?defs=PrepareTrainingAndTestTree&amp;project=cern">PrepareTrainingAndTestTree</a>( <a href="/source/s?defs=mycutSig&amp;project=cern">mycutSig</a>, <a href="/source/s?defs=mycutBkg&amp;project=cern">mycutBkg</a>,
<a class="l" name="216" href="#216">216</a>                                        <span class="s">"nTrain_Signal=0:nTrain_Background=0:SplitMode=Random:NormMode=NumEvents:!V"</span> )
<a class="l" name="217" href="#217">217</a>
<a class="l" name="218" href="#218">218</a>    <span class="c"># --------------------------------------------------------------------------------------------------</span>
<a class="l" name="219" href="#219">219</a>
<a class="hl" name="220" href="#220">220</a>    <span class="c"># ---- Book MVA methods</span>
<a class="l" name="221" href="#221">221</a>    <span class="c">#</span>
<a class="l" name="222" href="#222">222</a>    <span class="c"># please lookup the various method configuration options in the corresponding cxx files, eg:</span>
<a class="l" name="223" href="#223">223</a>    <span class="c"># <a href="/source/s?path=src/">src</a>/<a href="/source/s?path=src/MethoCuts.cxx">MethoCuts.cxx</a>, etc, or here: <a href="http://tmva.sourceforge.net/optionRef.html">http://tmva.sourceforge.net/optionRef.html</a></span>
<a class="l" name="224" href="#224">224</a>    <span class="c"># it is possible to preset ranges in the option string in which the cut optimisation should be done:</span>
<a class="l" name="225" href="#225">225</a>    <span class="c"># "...:CutRangeMin[2]=-1:CutRangeMax[2]=1"...", where [2] is the third input variable</span>
<a class="l" name="226" href="#226">226</a>
<a class="l" name="227" href="#227">227</a>    <span class="c"># Cut optimisation</span>
<a class="l" name="228" href="#228">228</a>    <b>if</b> <span class="s">"Cuts"</span> <b>in</b> <a href="/source/s?defs=mlist&amp;project=cern">mlist</a>:
<a class="l" name="229" href="#229">229</a>        <a href="/source/s?defs=factory&amp;project=cern">factory</a>.<a href="/source/s?defs=BookMethod&amp;project=cern">BookMethod</a>( <a class="d" href="#TMVA">TMVA</a>.<a href="/source/s?defs=Types&amp;project=cern">Types</a>.<a href="/source/s?defs=kCuts&amp;project=cern">kCuts</a>, <span class="s">"Cuts"</span>,
<a class="hl" name="230" href="#230">230</a>                            <span class="s">"!H:!V:FitMethod=MC:EffSel:SampleSize=200000:VarProp=FSmart"</span> )
<a class="l" name="231" href="#231">231</a>
<a class="l" name="232" href="#232">232</a>    <b>if</b> <span class="s">"CutsD"</span> <b>in</b> <a href="/source/s?defs=mlist&amp;project=cern">mlist</a>:
<a class="l" name="233" href="#233">233</a>        <a href="/source/s?defs=factory&amp;project=cern">factory</a>.<a href="/source/s?defs=BookMethod&amp;project=cern">BookMethod</a>( <a class="d" href="#TMVA">TMVA</a>.<a href="/source/s?defs=Types&amp;project=cern">Types</a>.<a href="/source/s?defs=kCuts&amp;project=cern">kCuts</a>, <span class="s">"CutsD"</span>,
<a class="l" name="234" href="#234">234</a>                            <span class="s">"!H:!V:FitMethod=MC:EffSel:SampleSize=200000:VarProp=FSmart:VarTransform=Decorrelate"</span> )
<a class="l" name="235" href="#235">235</a>
<a class="l" name="236" href="#236">236</a>    <b>if</b> <span class="s">"CutsPCA"</span> <b>in</b> <a href="/source/s?defs=mlist&amp;project=cern">mlist</a>:
<a class="l" name="237" href="#237">237</a>        <a href="/source/s?defs=factory&amp;project=cern">factory</a>.<a href="/source/s?defs=BookMethod&amp;project=cern">BookMethod</a>( <a class="d" href="#TMVA">TMVA</a>.<a href="/source/s?defs=Types&amp;project=cern">Types</a>.<a href="/source/s?defs=kCuts&amp;project=cern">kCuts</a>, <span class="s">"CutsPCA"</span>,
<a class="l" name="238" href="#238">238</a>                            <span class="s">"!H:!V:FitMethod=MC:EffSel:SampleSize=200000:VarProp=FSmart:VarTransform=PCA"</span> )
<a class="l" name="239" href="#239">239</a>
<a class="hl" name="240" href="#240">240</a>    <b>if</b> <span class="s">"CutsGA"</span> <b>in</b> <a href="/source/s?defs=mlist&amp;project=cern">mlist</a>:
<a class="l" name="241" href="#241">241</a>        <a href="/source/s?defs=factory&amp;project=cern">factory</a>.<a href="/source/s?defs=BookMethod&amp;project=cern">BookMethod</a>( <a class="d" href="#TMVA">TMVA</a>.<a href="/source/s?defs=Types&amp;project=cern">Types</a>.<a href="/source/s?defs=kCuts&amp;project=cern">kCuts</a>, <span class="s">"CutsGA"</span>,
<a class="l" name="242" href="#242">242</a>                            <span class="s">"H:!V:FitMethod=GA:CutRangeMin[0]=-10:CutRangeMax[0]=10:VarProp[1]=FMax:EffSel:Steps=30:Cycles=3:PopSize=400:SC_steps=10:SC_rate=5:SC_factor=0.95"</span> )
<a class="l" name="243" href="#243">243</a>
<a class="l" name="244" href="#244">244</a>    <b>if</b> <span class="s">"CutsSA"</span> <b>in</b> <a href="/source/s?defs=mlist&amp;project=cern">mlist</a>:
<a class="l" name="245" href="#245">245</a>        <a href="/source/s?defs=factory&amp;project=cern">factory</a>.<a href="/source/s?defs=BookMethod&amp;project=cern">BookMethod</a>( <a class="d" href="#TMVA">TMVA</a>.<a href="/source/s?defs=Types&amp;project=cern">Types</a>.<a href="/source/s?defs=kCuts&amp;project=cern">kCuts</a>, <span class="s">"CutsSA"</span>,
<a class="l" name="246" href="#246">246</a>                            <span class="s">"!H:!V:FitMethod=SA:EffSel:MaxCalls=150000:KernelTemp=IncAdaptive:InitialTemp=1e+6:MinTemp=1e-6:Eps=1e-10:UseDefaultScale"</span> )
<a class="l" name="247" href="#247">247</a>
<a class="l" name="248" href="#248">248</a>    <span class="c"># Likelihood ("naive Bayes estimator")</span>
<a class="l" name="249" href="#249">249</a>    <b>if</b> <span class="s">"Likelihood"</span> <b>in</b> <a href="/source/s?defs=mlist&amp;project=cern">mlist</a>:
<a class="hl" name="250" href="#250">250</a>        <a href="/source/s?defs=factory&amp;project=cern">factory</a>.<a href="/source/s?defs=BookMethod&amp;project=cern">BookMethod</a>( <a class="d" href="#TMVA">TMVA</a>.<a href="/source/s?defs=Types&amp;project=cern">Types</a>.<a href="/source/s?defs=kLikelihood&amp;project=cern">kLikelihood</a>, <span class="s">"Likelihood"</span>,
<a class="l" name="251" href="#251">251</a>                            <span class="s">"H:!V:!TransformOutput:PDFInterpol=Spline2:NSmoothSig[0]=20:NSmoothBkg[0]=20:NSmoothBkg[1]=10:NSmooth=1:NAvEvtPerBin=50"</span> )
<a class="l" name="252" href="#252">252</a>
<a class="l" name="253" href="#253">253</a>    <span class="c"># Decorrelated likelihood</span>
<a class="l" name="254" href="#254">254</a>    <b>if</b> <span class="s">"LikelihoodD"</span> <b>in</b> <a href="/source/s?defs=mlist&amp;project=cern">mlist</a>:
<a class="l" name="255" href="#255">255</a>        <a href="/source/s?defs=factory&amp;project=cern">factory</a>.<a href="/source/s?defs=BookMethod&amp;project=cern">BookMethod</a>( <a class="d" href="#TMVA">TMVA</a>.<a href="/source/s?defs=Types&amp;project=cern">Types</a>.<a href="/source/s?defs=kLikelihood&amp;project=cern">kLikelihood</a>, <span class="s">"LikelihoodD"</span>,
<a class="l" name="256" href="#256">256</a>                            <span class="s">"!H:!V:TransformOutput:PDFInterpol=Spline2:NSmoothSig[0]=20:NSmoothBkg[0]=20:NSmooth=5:NAvEvtPerBin=50:VarTransform=Decorrelate"</span> )
<a class="l" name="257" href="#257">257</a>
<a class="l" name="258" href="#258">258</a>    <span class="c"># PCA-transformed likelihood</span>
<a class="l" name="259" href="#259">259</a>    <b>if</b> <span class="s">"LikelihoodPCA"</span> <b>in</b> <a href="/source/s?defs=mlist&amp;project=cern">mlist</a>:
<a class="hl" name="260" href="#260">260</a>        <a href="/source/s?defs=factory&amp;project=cern">factory</a>.<a href="/source/s?defs=BookMethod&amp;project=cern">BookMethod</a>( <a class="d" href="#TMVA">TMVA</a>.<a href="/source/s?defs=Types&amp;project=cern">Types</a>.<a href="/source/s?defs=kLikelihood&amp;project=cern">kLikelihood</a>, <span class="s">"LikelihoodPCA"</span>,
<a class="l" name="261" href="#261">261</a>                            <span class="s">"!H:!V:!TransformOutput:PDFInterpol=Spline2:NSmoothSig[0]=20:NSmoothBkg[0]=20:NSmooth=5:NAvEvtPerBin=50:VarTransform=PCA"</span> )
<a class="l" name="262" href="#262">262</a>
<a class="l" name="263" href="#263">263</a>    <span class="c"># Use a kernel density estimator to approximate the PDFs</span>
<a class="l" name="264" href="#264">264</a>    <b>if</b> <span class="s">"LikelihoodKDE"</span> <b>in</b> <a href="/source/s?defs=mlist&amp;project=cern">mlist</a>:
<a class="l" name="265" href="#265">265</a>        <a href="/source/s?defs=factory&amp;project=cern">factory</a>.<a href="/source/s?defs=BookMethod&amp;project=cern">BookMethod</a>( <a class="d" href="#TMVA">TMVA</a>.<a href="/source/s?defs=Types&amp;project=cern">Types</a>.<a href="/source/s?defs=kLikelihood&amp;project=cern">kLikelihood</a>, <span class="s">"LikelihoodKDE"</span>,
<a class="l" name="266" href="#266">266</a>                            <span class="s">"!H:!V:!TransformOutput:PDFInterpol=KDE:KDEtype=Gauss:KDEiter=Adaptive:KDEFineFactor=0.3:KDEborder=None:NAvEvtPerBin=50"</span> )
<a class="l" name="267" href="#267">267</a>
<a class="l" name="268" href="#268">268</a>    <span class="c"># Use a variable-dependent mix of splines and kernel density estimator</span>
<a class="l" name="269" href="#269">269</a>    <b>if</b> <span class="s">"LikelihoodMIX"</span> <b>in</b> <a href="/source/s?defs=mlist&amp;project=cern">mlist</a>:
<a class="hl" name="270" href="#270">270</a>        <a href="/source/s?defs=factory&amp;project=cern">factory</a>.<a href="/source/s?defs=BookMethod&amp;project=cern">BookMethod</a>( <a class="d" href="#TMVA">TMVA</a>.<a href="/source/s?defs=Types&amp;project=cern">Types</a>.<a href="/source/s?defs=kLikelihood&amp;project=cern">kLikelihood</a>, <span class="s">"LikelihoodMIX"</span>,
<a class="l" name="271" href="#271">271</a>                            <span class="s">"!H:!V:!TransformOutput:PDFInterpolSig[0]=KDE:PDFInterpolBkg[0]=KDE:PDFInterpolSig[1]=KDE:PDFInterpolBkg[1]=KDE:PDFInterpolSig[2]=Spline2:PDFInterpolBkg[2]=Spline2:PDFInterpolSig[3]=Spline2:PDFInterpolBkg[3]=Spline2:KDEtype=Gauss:KDEiter=Nonadaptive:KDEborder=None:NAvEvtPerBin=50"</span> )
<a class="l" name="272" href="#272">272</a>
<a class="l" name="273" href="#273">273</a>    <span class="c"># Test the multi-dimensional probability density estimator</span>
<a class="l" name="274" href="#274">274</a>    <span class="c"># here are the options strings for the MinMax and RMS methods, respectively:</span>
<a class="l" name="275" href="#275">275</a>    <span class="c">#      "!H:!V:VolumeRangeMode=MinMax:DeltaFrac=0.2:KernelEstimator=Gauss:GaussSigma=0.3" );</span>
<a class="l" name="276" href="#276">276</a>    <span class="c">#      "!H:!V:VolumeRangeMode=RMS:DeltaFrac=3:KernelEstimator=Gauss:GaussSigma=0.3" );</span>
<a class="l" name="277" href="#277">277</a>    <b>if</b> <span class="s">"PDERS"</span> <b>in</b> <a href="/source/s?defs=mlist&amp;project=cern">mlist</a>:
<a class="l" name="278" href="#278">278</a>        <a href="/source/s?defs=factory&amp;project=cern">factory</a>.<a href="/source/s?defs=BookMethod&amp;project=cern">BookMethod</a>( <a class="d" href="#TMVA">TMVA</a>.<a href="/source/s?defs=Types&amp;project=cern">Types</a>.<a href="/source/s?defs=kPDERS&amp;project=cern">kPDERS</a>, <span class="s">"PDERS"</span>,
<a class="l" name="279" href="#279">279</a>                            <span class="s">"!H:!V:NormTree=T:VolumeRangeMode=Adaptive:KernelEstimator=Gauss:GaussSigma=0.3:NEventsMin=400:NEventsMax=600"</span> )
<a class="hl" name="280" href="#280">280</a>
<a class="l" name="281" href="#281">281</a>    <b>if</b> <span class="s">"PDERSD"</span> <b>in</b> <a href="/source/s?defs=mlist&amp;project=cern">mlist</a>:
<a class="l" name="282" href="#282">282</a>        <a href="/source/s?defs=factory&amp;project=cern">factory</a>.<a href="/source/s?defs=BookMethod&amp;project=cern">BookMethod</a>( <a class="d" href="#TMVA">TMVA</a>.<a href="/source/s?defs=Types&amp;project=cern">Types</a>.<a href="/source/s?defs=kPDERS&amp;project=cern">kPDERS</a>, <span class="s">"PDERSD"</span>,
<a class="l" name="283" href="#283">283</a>                            <span class="s">"!H:!V:VolumeRangeMode=Adaptive:KernelEstimator=Gauss:GaussSigma=0.3:NEventsMin=400:NEventsMax=600:VarTransform=Decorrelate"</span> )
<a class="l" name="284" href="#284">284</a>
<a class="l" name="285" href="#285">285</a>    <b>if</b> <span class="s">"PDERSPCA"</span> <b>in</b> <a href="/source/s?defs=mlist&amp;project=cern">mlist</a>:
<a class="l" name="286" href="#286">286</a>        <a href="/source/s?defs=factory&amp;project=cern">factory</a>.<a href="/source/s?defs=BookMethod&amp;project=cern">BookMethod</a>( <a class="d" href="#TMVA">TMVA</a>.<a href="/source/s?defs=Types&amp;project=cern">Types</a>.<a href="/source/s?defs=kPDERS&amp;project=cern">kPDERS</a>, <span class="s">"PDERSPCA"</span>,
<a class="l" name="287" href="#287">287</a>                             <span class="s">"!H:!V:VolumeRangeMode=Adaptive:KernelEstimator=Gauss:GaussSigma=0.3:NEventsMin=400:NEventsMax=600:VarTransform=PCA"</span> )
<a class="l" name="288" href="#288">288</a>
<a class="l" name="289" href="#289">289</a>   <span class="c"># Multi-dimensional likelihood estimator using self-adapting phase-space binning</span>
<a class="hl" name="290" href="#290">290</a>    <b>if</b> <span class="s">"PDEFoam"</span> <b>in</b> <a href="/source/s?defs=mlist&amp;project=cern">mlist</a>:
<a class="l" name="291" href="#291">291</a>        <a href="/source/s?defs=factory&amp;project=cern">factory</a>.<a href="/source/s?defs=BookMethod&amp;project=cern">BookMethod</a>( <a class="d" href="#TMVA">TMVA</a>.<a href="/source/s?defs=Types&amp;project=cern">Types</a>.<a href="/source/s?defs=kPDEFoam&amp;project=cern">kPDEFoam</a>, <span class="s">"PDEFoam"</span>,
<a class="l" name="292" href="#292">292</a>                            <span class="s">"!H:!V:SigBgSeparate=F:TailCut=0.001:VolFrac=0.0666:nActiveCells=500:nSampl=2000:nBin=5:Nmin=100:Kernel=None:Compress=T"</span> )
<a class="l" name="293" href="#293">293</a>
<a class="l" name="294" href="#294">294</a>    <b>if</b> <span class="s">"PDEFoamBoost"</span> <b>in</b> <a href="/source/s?defs=mlist&amp;project=cern">mlist</a>:
<a class="l" name="295" href="#295">295</a>        <a href="/source/s?defs=factory&amp;project=cern">factory</a>.<a href="/source/s?defs=BookMethod&amp;project=cern">BookMethod</a>( <a class="d" href="#TMVA">TMVA</a>.<a href="/source/s?defs=Types&amp;project=cern">Types</a>.<a href="/source/s?defs=kPDEFoam&amp;project=cern">kPDEFoam</a>, <span class="s">"PDEFoamBoost"</span>,
<a class="l" name="296" href="#296">296</a>                            <span class="s">"!H:!V:Boost_Num=30:Boost_Transform=linear:SigBgSeparate=F:MaxDepth=4:UseYesNoCell=T:DTLogic=MisClassificationError:FillFoamWithOrigWeights=F:TailCut=0:nActiveCells=500:nBin=20:Nmin=400:Kernel=None:Compress=T"</span> )
<a class="l" name="297" href="#297">297</a>
<a class="l" name="298" href="#298">298</a>    <span class="c"># K-Nearest Neighbour classifier (KNN)</span>
<a class="l" name="299" href="#299">299</a>    <b>if</b> <span class="s">"KNN"</span> <b>in</b> <a href="/source/s?defs=mlist&amp;project=cern">mlist</a>:
<a class="hl" name="300" href="#300">300</a>        <a href="/source/s?defs=factory&amp;project=cern">factory</a>.<a href="/source/s?defs=BookMethod&amp;project=cern">BookMethod</a>( <a class="d" href="#TMVA">TMVA</a>.<a href="/source/s?defs=Types&amp;project=cern">Types</a>.<a href="/source/s?defs=kKNN&amp;project=cern">kKNN</a>, <span class="s">"KNN"</span>,
<a class="l" name="301" href="#301">301</a>                            <span class="s">"H:nkNN=20:ScaleFrac=0.8:SigmaFact=1.0:Kernel=Gaus:UseKernel=F:UseWeight=T:!Trim"</span> )
<a class="l" name="302" href="#302">302</a>
<a class="l" name="303" href="#303">303</a>    <span class="c"># H-Matrix (chi2-squared) method</span>
<a class="l" name="304" href="#304">304</a>    <b>if</b> <span class="s">"HMatrix"</span> <b>in</b> <a href="/source/s?defs=mlist&amp;project=cern">mlist</a>:
<a class="l" name="305" href="#305">305</a>        <a href="/source/s?defs=factory&amp;project=cern">factory</a>.<a href="/source/s?defs=BookMethod&amp;project=cern">BookMethod</a>( <a class="d" href="#TMVA">TMVA</a>.<a href="/source/s?defs=Types&amp;project=cern">Types</a>.<a href="/source/s?defs=kHMatrix&amp;project=cern">kHMatrix</a>, <span class="s">"HMatrix"</span>, <span class="s">"!H:!V"</span> )
<a class="l" name="306" href="#306">306</a>
<a class="l" name="307" href="#307">307</a>    <span class="c"># Linear discriminant (same as Fisher discriminant)</span>
<a class="l" name="308" href="#308">308</a>    <b>if</b> <span class="s">"LD"</span> <b>in</b> <a href="/source/s?defs=mlist&amp;project=cern">mlist</a>:
<a class="l" name="309" href="#309">309</a>        <a href="/source/s?defs=factory&amp;project=cern">factory</a>.<a href="/source/s?defs=BookMethod&amp;project=cern">BookMethod</a>( <a class="d" href="#TMVA">TMVA</a>.<a href="/source/s?defs=Types&amp;project=cern">Types</a>.<a href="/source/s?defs=kLD&amp;project=cern">kLD</a>, <span class="s">"LD"</span>, <span class="s">"H:!V:VarTransform=None:CreateMVAPdfs:PDFInterpolMVAPdf=Spline2:NbinsMVAPdf=50:NsmoothMVAPdf=10"</span> )
<a class="hl" name="310" href="#310">310</a>
<a class="l" name="311" href="#311">311</a>    <span class="c"># Fisher discriminant (same as LD)</span>
<a class="l" name="312" href="#312">312</a>    <b>if</b> <span class="s">"Fisher"</span> <b>in</b> <a href="/source/s?defs=mlist&amp;project=cern">mlist</a>:
<a class="l" name="313" href="#313">313</a>        <a href="/source/s?defs=factory&amp;project=cern">factory</a>.<a href="/source/s?defs=BookMethod&amp;project=cern">BookMethod</a>( <a class="d" href="#TMVA">TMVA</a>.<a href="/source/s?defs=Types&amp;project=cern">Types</a>.<a href="/source/s?defs=kFisher&amp;project=cern">kFisher</a>, <span class="s">"Fisher"</span>, <span class="s">"H:!V:Fisher:CreateMVAPdfs:PDFInterpolMVAPdf=Spline2:NbinsMVAPdf=50:NsmoothMVAPdf=10"</span> )
<a class="l" name="314" href="#314">314</a>
<a class="l" name="315" href="#315">315</a>    <span class="c"># Fisher with Gauss-transformed input variables</span>
<a class="l" name="316" href="#316">316</a>    <b>if</b> <span class="s">"FisherG"</span> <b>in</b> <a href="/source/s?defs=mlist&amp;project=cern">mlist</a>:
<a class="l" name="317" href="#317">317</a>        <a href="/source/s?defs=factory&amp;project=cern">factory</a>.<a href="/source/s?defs=BookMethod&amp;project=cern">BookMethod</a>( <a class="d" href="#TMVA">TMVA</a>.<a href="/source/s?defs=Types&amp;project=cern">Types</a>.<a href="/source/s?defs=kFisher&amp;project=cern">kFisher</a>, <span class="s">"FisherG"</span>, <span class="s">"H:!V:VarTransform=Gauss"</span> )
<a class="l" name="318" href="#318">318</a>
<a class="l" name="319" href="#319">319</a>    <span class="c"># Composite classifier: ensemble (tree) of boosted Fisher classifiers</span>
<a class="hl" name="320" href="#320">320</a>    <b>if</b> <span class="s">"BoostedFisher"</span> <b>in</b> <a href="/source/s?defs=mlist&amp;project=cern">mlist</a>:
<a class="l" name="321" href="#321">321</a>        <a href="/source/s?defs=factory&amp;project=cern">factory</a>.<a href="/source/s?defs=BookMethod&amp;project=cern">BookMethod</a>( <a class="d" href="#TMVA">TMVA</a>.<a href="/source/s?defs=Types&amp;project=cern">Types</a>.<a href="/source/s?defs=kFisher&amp;project=cern">kFisher</a>, <span class="s">"BoostedFisher"</span>,
<a class="l" name="322" href="#322">322</a>                            <span class="s">"H:!V:Boost_Num=20:Boost_Transform=log:Boost_Type=AdaBoost:Boost_AdaBoostBeta=0.2"</span> )
<a class="l" name="323" href="#323">323</a>
<a class="l" name="324" href="#324">324</a>    <span class="c"># Function discrimination analysis (FDA) -- test of various fitters - the recommended one is Minuit (or GA or SA)</span>
<a class="l" name="325" href="#325">325</a>    <b>if</b> <span class="s">"FDA_MC"</span> <b>in</b> <a href="/source/s?defs=mlist&amp;project=cern">mlist</a>:
<a class="l" name="326" href="#326">326</a>        <a href="/source/s?defs=factory&amp;project=cern">factory</a>.<a href="/source/s?defs=BookMethod&amp;project=cern">BookMethod</a>( <a class="d" href="#TMVA">TMVA</a>.<a href="/source/s?defs=Types&amp;project=cern">Types</a>.<a href="/source/s?defs=kFDA&amp;project=cern">kFDA</a>, <span class="s">"FDA_MC"</span>,
<a class="l" name="327" href="#327">327</a>                            <span class="s">"H:!V:Formula=(0)+(1)*x0+(2)*x1+(3)*x2+(4)*x3:ParRanges=(-1,1)(-10,10);(-10,10);(-10,10);(-10,10):FitMethod=MC:SampleSize=100000:Sigma=0.1"</span> );
<a class="l" name="328" href="#328">328</a>
<a class="l" name="329" href="#329">329</a>    <b>if</b> <span class="s">"FDA_GA"</span> <b>in</b> <a href="/source/s?defs=mlist&amp;project=cern">mlist</a>:
<a class="hl" name="330" href="#330">330</a>        <a href="/source/s?defs=factory&amp;project=cern">factory</a>.<a href="/source/s?defs=BookMethod&amp;project=cern">BookMethod</a>( <a class="d" href="#TMVA">TMVA</a>.<a href="/source/s?defs=Types&amp;project=cern">Types</a>.<a href="/source/s?defs=kFDA&amp;project=cern">kFDA</a>, <span class="s">"FDA_GA"</span>,
<a class="l" name="331" href="#331">331</a>                            <span class="s">"H:!V:Formula=(0)+(1)*x0+(2)*x1+(3)*x2+(4)*x3:ParRanges=(-1,1)(-10,10);(-10,10);(-10,10);(-10,10):FitMethod=GA:PopSize=300:Cycles=3:Steps=20:Trim=True:SaveBestGen=1"</span> );
<a class="l" name="332" href="#332">332</a>
<a class="l" name="333" href="#333">333</a>    <b>if</b> <span class="s">"FDA_SA"</span> <b>in</b> <a href="/source/s?defs=mlist&amp;project=cern">mlist</a>:
<a class="l" name="334" href="#334">334</a>        <a href="/source/s?defs=factory&amp;project=cern">factory</a>.<a href="/source/s?defs=BookMethod&amp;project=cern">BookMethod</a>( <a class="d" href="#TMVA">TMVA</a>.<a href="/source/s?defs=Types&amp;project=cern">Types</a>.<a href="/source/s?defs=kFDA&amp;project=cern">kFDA</a>, <span class="s">"FDA_SA"</span>,
<a class="l" name="335" href="#335">335</a>                            <span class="s">"H:!V:Formula=(0)+(1)*x0+(2)*x1+(3)*x2+(4)*x3:ParRanges=(-1,1)(-10,10);(-10,10);(-10,10);(-10,10):FitMethod=SA:MaxCalls=15000:KernelTemp=IncAdaptive:InitialTemp=1e+6:MinTemp=1e-6:Eps=1e-10:UseDefaultScale"</span> );
<a class="l" name="336" href="#336">336</a>
<a class="l" name="337" href="#337">337</a>    <b>if</b> <span class="s">"FDA_MT"</span> <b>in</b> <a href="/source/s?defs=mlist&amp;project=cern">mlist</a>:
<a class="l" name="338" href="#338">338</a>        <a href="/source/s?defs=factory&amp;project=cern">factory</a>.<a href="/source/s?defs=BookMethod&amp;project=cern">BookMethod</a>( <a class="d" href="#TMVA">TMVA</a>.<a href="/source/s?defs=Types&amp;project=cern">Types</a>.<a href="/source/s?defs=kFDA&amp;project=cern">kFDA</a>, <span class="s">"FDA_MT"</span>,
<a class="l" name="339" href="#339">339</a>                            <span class="s">"H:!V:Formula=(0)+(1)*x0+(2)*x1+(3)*x2+(4)*x3:ParRanges=(-1,1)(-10,10);(-10,10);(-10,10);(-10,10):FitMethod=MINUIT:ErrorLevel=1:PrintLevel=-1:FitStrategy=2:UseImprove:UseMinos:SetBatch"</span> );
<a class="hl" name="340" href="#340">340</a>
<a class="l" name="341" href="#341">341</a>    <b>if</b> <span class="s">"FDA_GAMT"</span> <b>in</b> <a href="/source/s?defs=mlist&amp;project=cern">mlist</a>:
<a class="l" name="342" href="#342">342</a>        <a href="/source/s?defs=factory&amp;project=cern">factory</a>.<a href="/source/s?defs=BookMethod&amp;project=cern">BookMethod</a>( <a class="d" href="#TMVA">TMVA</a>.<a href="/source/s?defs=Types&amp;project=cern">Types</a>.<a href="/source/s?defs=kFDA&amp;project=cern">kFDA</a>, <span class="s">"FDA_GAMT"</span>,
<a class="l" name="343" href="#343">343</a>                            <span class="s">"H:!V:Formula=(0)+(1)*x0+(2)*x1+(3)*x2+(4)*x3:ParRanges=(-1,1)(-10,10);(-10,10);(-10,10);(-10,10):FitMethod=GA:Converger=MINUIT:ErrorLevel=1:PrintLevel=-1:FitStrategy=0:!UseImprove:!UseMinos:SetBatch:Cycles=1:PopSize=5:Steps=5:Trim"</span> );
<a class="l" name="344" href="#344">344</a>
<a class="l" name="345" href="#345">345</a>    <b>if</b> <span class="s">"FDA_MCMT"</span> <b>in</b> <a href="/source/s?defs=mlist&amp;project=cern">mlist</a>:
<a class="l" name="346" href="#346">346</a>        <a href="/source/s?defs=factory&amp;project=cern">factory</a>.<a href="/source/s?defs=BookMethod&amp;project=cern">BookMethod</a>( <a class="d" href="#TMVA">TMVA</a>.<a href="/source/s?defs=Types&amp;project=cern">Types</a>.<a href="/source/s?defs=kFDA&amp;project=cern">kFDA</a>, <span class="s">"FDA_MCMT"</span>,
<a class="l" name="347" href="#347">347</a>                            <span class="s">"H:!V:Formula=(0)+(1)*x0+(2)*x1+(3)*x2+(4)*x3:ParRanges=(-1,1)(-10,10);(-10,10);(-10,10);(-10,10):FitMethod=MC:Converger=MINUIT:ErrorLevel=1:PrintLevel=-1:FitStrategy=0:!UseImprove:!UseMinos:SetBatch:SampleSize=20"</span> );
<a class="l" name="348" href="#348">348</a>
<a class="l" name="349" href="#349">349</a>    <span class="c"># TMVA ANN: MLP (recommended ANN) -- all ANNs in TMVA are Multilayer Perceptrons</span>
<a class="hl" name="350" href="#350">350</a>    <b>if</b> <span class="s">"MLP"</span> <b>in</b> <a href="/source/s?defs=mlist&amp;project=cern">mlist</a>:
<a class="l" name="351" href="#351">351</a>        <a href="/source/s?defs=factory&amp;project=cern">factory</a>.<a href="/source/s?defs=BookMethod&amp;project=cern">BookMethod</a>( <a class="d" href="#TMVA">TMVA</a>.<a href="/source/s?defs=Types&amp;project=cern">Types</a>.<a href="/source/s?defs=kMLP&amp;project=cern">kMLP</a>, <span class="s">"MLP"</span>, <span class="s">"H:!V:NeuronType=tanh:VarTransform=N:NCycles=600:HiddenLayers=N+5:TestRate=5:!UseRegulator"</span> )
<a class="l" name="352" href="#352">352</a>
<a class="l" name="353" href="#353">353</a>    <b>if</b> <span class="s">"MLPBFGS"</span> <b>in</b> <a href="/source/s?defs=mlist&amp;project=cern">mlist</a>:
<a class="l" name="354" href="#354">354</a>        <a href="/source/s?defs=factory&amp;project=cern">factory</a>.<a href="/source/s?defs=BookMethod&amp;project=cern">BookMethod</a>( <a class="d" href="#TMVA">TMVA</a>.<a href="/source/s?defs=Types&amp;project=cern">Types</a>.<a href="/source/s?defs=kMLP&amp;project=cern">kMLP</a>, <span class="s">"MLPBFGS"</span>, <span class="s">"H:!V:NeuronType=tanh:VarTransform=N:NCycles=600:HiddenLayers=N+5:TestRate=5:TrainingMethod=BFGS:!UseRegulator"</span> )
<a class="l" name="355" href="#355">355</a>
<a class="l" name="356" href="#356">356</a>    <b>if</b> <span class="s">"MLPBNN"</span> <b>in</b> <a href="/source/s?defs=mlist&amp;project=cern">mlist</a>:
<a class="l" name="357" href="#357">357</a>        <a href="/source/s?defs=factory&amp;project=cern">factory</a>.<a href="/source/s?defs=BookMethod&amp;project=cern">BookMethod</a>( <a class="d" href="#TMVA">TMVA</a>.<a href="/source/s?defs=Types&amp;project=cern">Types</a>.<a href="/source/s?defs=kMLP&amp;project=cern">kMLP</a>, <span class="s">"MLPBNN"</span>, <span class="s">"H:!V:NeuronType=tanh:VarTransform=N:NCycles=600:HiddenLayers=N+5:TestRate=5:TrainingMethod=BFGS:UseRegulator"</span> ) <span class="c"># BFGS training with bayesian regulators</span>
<a class="l" name="358" href="#358">358</a>
<a class="l" name="359" href="#359">359</a>    <span class="c"># CF(Clermont-Ferrand)ANN</span>
<a class="hl" name="360" href="#360">360</a>    <b>if</b> <span class="s">"CFMlpANN"</span> <b>in</b> <a href="/source/s?defs=mlist&amp;project=cern">mlist</a>:
<a class="l" name="361" href="#361">361</a>        <a href="/source/s?defs=factory&amp;project=cern">factory</a>.<a href="/source/s?defs=BookMethod&amp;project=cern">BookMethod</a>( <a class="d" href="#TMVA">TMVA</a>.<a href="/source/s?defs=Types&amp;project=cern">Types</a>.<a href="/source/s?defs=kCFMlpANN&amp;project=cern">kCFMlpANN</a>, <span class="s">"CFMlpANN"</span>, <span class="s">"!H:!V:NCycles=2000:HiddenLayers=N+1,N"</span>  ) <span class="c"># n_cycles:#nodes:#nodes:...</span>
<a class="l" name="362" href="#362">362</a>
<a class="l" name="363" href="#363">363</a>    <span class="c"># Tmlp(Root)ANN</span>
<a class="l" name="364" href="#364">364</a>    <b>if</b> <span class="s">"TMlpANN"</span> <b>in</b> <a href="/source/s?defs=mlist&amp;project=cern">mlist</a>:
<a class="l" name="365" href="#365">365</a>        <a href="/source/s?defs=factory&amp;project=cern">factory</a>.<a href="/source/s?defs=BookMethod&amp;project=cern">BookMethod</a>( <a class="d" href="#TMVA">TMVA</a>.<a href="/source/s?defs=Types&amp;project=cern">Types</a>.<a href="/source/s?defs=kTMlpANN&amp;project=cern">kTMlpANN</a>, <span class="s">"TMlpANN"</span>, <span class="s">"!H:!V:NCycles=200:HiddenLayers=N+1,N:LearningMethod=BFGS:ValidationFraction=0.3"</span>  ) <span class="c"># n_cycles:#nodes:#nodes:...</span>
<a class="l" name="366" href="#366">366</a>
<a class="l" name="367" href="#367">367</a>    <span class="c"># Support Vector Machine</span>
<a class="l" name="368" href="#368">368</a>    <b>if</b> <span class="s">"SVM"</span> <b>in</b> <a href="/source/s?defs=mlist&amp;project=cern">mlist</a>:
<a class="l" name="369" href="#369">369</a>        <a href="/source/s?defs=factory&amp;project=cern">factory</a>.<a href="/source/s?defs=BookMethod&amp;project=cern">BookMethod</a>( <a class="d" href="#TMVA">TMVA</a>.<a href="/source/s?defs=Types&amp;project=cern">Types</a>.<a href="/source/s?defs=kSVM&amp;project=cern">kSVM</a>, <span class="s">"SVM"</span>, <span class="s">"Gamma=0.25:Tol=0.001:VarTransform=Norm"</span> )
<a class="hl" name="370" href="#370">370</a>
<a class="l" name="371" href="#371">371</a>    <span class="c"># Boosted Decision Trees</span>
<a class="l" name="372" href="#372">372</a>    <b>if</b> <span class="s">"BDTG"</span> <b>in</b> <a href="/source/s?defs=mlist&amp;project=cern">mlist</a>:
<a class="l" name="373" href="#373">373</a>        <a href="/source/s?defs=factory&amp;project=cern">factory</a>.<a href="/source/s?defs=BookMethod&amp;project=cern">BookMethod</a>( <a class="d" href="#TMVA">TMVA</a>.<a href="/source/s?defs=Types&amp;project=cern">Types</a>.<a href="/source/s?defs=kBDT&amp;project=cern">kBDT</a>, <span class="s">"BDTG"</span>,
<a class="l" name="374" href="#374">374</a>                            <span class="s">"!H:!V:NTrees=1000:MinNodeSize=1.5%:BoostType=Grad:Shrinkage=0.10:UseBaggedGrad:GradBaggingFraction=0.5:nCuts=20:MaxDepth=2"</span> )
<a class="l" name="375" href="#375">375</a>
<a class="l" name="376" href="#376">376</a>    <b>if</b> <span class="s">"BDT"</span> <b>in</b> <a href="/source/s?defs=mlist&amp;project=cern">mlist</a>:
<a class="l" name="377" href="#377">377</a>        <a href="/source/s?defs=factory&amp;project=cern">factory</a>.<a href="/source/s?defs=BookMethod&amp;project=cern">BookMethod</a>( <a class="d" href="#TMVA">TMVA</a>.<a href="/source/s?defs=Types&amp;project=cern">Types</a>.<a href="/source/s?defs=kBDT&amp;project=cern">kBDT</a>, <span class="s">"BDT"</span>,
<a class="l" name="378" href="#378">378</a>                           <span class="s">"!H:!V:NTrees=850:MinNodeSize=2.5%:MaxDepth=3:BoostType=AdaBoost:AdaBoostBeta=0.5:SeparationType=GiniIndex:nCuts=20"</span> )
<a class="l" name="379" href="#379">379</a>
<a class="hl" name="380" href="#380">380</a>    <b>if</b> <span class="s">"BDTB"</span> <b>in</b> <a href="/source/s?defs=mlist&amp;project=cern">mlist</a>:
<a class="l" name="381" href="#381">381</a>        <a href="/source/s?defs=factory&amp;project=cern">factory</a>.<a href="/source/s?defs=BookMethod&amp;project=cern">BookMethod</a>( <a class="d" href="#TMVA">TMVA</a>.<a href="/source/s?defs=Types&amp;project=cern">Types</a>.<a href="/source/s?defs=kBDT&amp;project=cern">kBDT</a>, <span class="s">"BDTB"</span>,
<a class="l" name="382" href="#382">382</a>                           <span class="s">"!H:!V:NTrees=400:BoostType=Bagging:SeparationType=GiniIndex:nCuts=20"</span> )
<a class="l" name="383" href="#383">383</a>
<a class="l" name="384" href="#384">384</a>    <b>if</b> <span class="s">"BDTD"</span> <b>in</b> <a href="/source/s?defs=mlist&amp;project=cern">mlist</a>:
<a class="l" name="385" href="#385">385</a>        <a href="/source/s?defs=factory&amp;project=cern">factory</a>.<a href="/source/s?defs=BookMethod&amp;project=cern">BookMethod</a>( <a class="d" href="#TMVA">TMVA</a>.<a href="/source/s?defs=Types&amp;project=cern">Types</a>.<a href="/source/s?defs=kBDT&amp;project=cern">kBDT</a>, <span class="s">"BDTD"</span>,
<a class="l" name="386" href="#386">386</a>                           <span class="s">"!H:!V:NTrees=400:MinNodeSize=5%:MaxDepth=3:BoostType=AdaBoost:SeparationType=GiniIndex:nCuts=20:VarTransform=Decorrelate"</span> )
<a class="l" name="387" href="#387">387</a>
<a class="l" name="388" href="#388">388</a>    <span class="c"># RuleFit -- TMVA implementation of Friedman's method</span>
<a class="l" name="389" href="#389">389</a>    <b>if</b> <span class="s">"RuleFit"</span> <b>in</b> <a href="/source/s?defs=mlist&amp;project=cern">mlist</a>:
<a class="hl" name="390" href="#390">390</a>        <a href="/source/s?defs=factory&amp;project=cern">factory</a>.<a href="/source/s?defs=BookMethod&amp;project=cern">BookMethod</a>( <a class="d" href="#TMVA">TMVA</a>.<a href="/source/s?defs=Types&amp;project=cern">Types</a>.<a href="/source/s?defs=kRuleFit&amp;project=cern">kRuleFit</a>, <span class="s">"RuleFit"</span>,
<a class="l" name="391" href="#391">391</a>                            <span class="s">"H:!V:RuleFitModule=RFTMVA:Model=ModRuleLinear:MinImp=0.001:RuleMinDist=0.001:NTrees=20:fEventsMin=0.01:fEventsMax=0.5:GDTau=-1.0:GDTauPrec=0.01:GDStep=0.01:GDNSteps=10000:GDErrScale=1.02"</span> )
<a class="l" name="392" href="#392">392</a>
<a class="l" name="393" href="#393">393</a>    <span class="c"># --------------------------------------------------------------------------------------------------</span>
<a class="l" name="394" href="#394">394</a>
<a class="l" name="395" href="#395">395</a>    <span class="c"># ---- Now you can tell the factory to train, test, and evaluate the MVAs.</span>
<a class="l" name="396" href="#396">396</a>
<a class="l" name="397" href="#397">397</a>    <span class="c"># Train MVAs</span>
<a class="l" name="398" href="#398">398</a>    <a href="/source/s?defs=factory&amp;project=cern">factory</a>.<a href="/source/s?defs=TrainAllMethods&amp;project=cern">TrainAllMethods</a>()
<a class="l" name="399" href="#399">399</a>
<a class="hl" name="400" href="#400">400</a>    <span class="c"># Test MVAs</span>
<a class="l" name="401" href="#401">401</a>    <a href="/source/s?defs=factory&amp;project=cern">factory</a>.<a href="/source/s?defs=TestAllMethods&amp;project=cern">TestAllMethods</a>()
<a class="l" name="402" href="#402">402</a>
<a class="l" name="403" href="#403">403</a>    <span class="c"># Evaluate MVAs</span>
<a class="l" name="404" href="#404">404</a>    <a href="/source/s?defs=factory&amp;project=cern">factory</a>.<a href="/source/s?defs=EvaluateAllMethods&amp;project=cern">EvaluateAllMethods</a>()
<a class="l" name="405" href="#405">405</a>
<a class="l" name="406" href="#406">406</a>    <span class="c"># Save the output.</span>
<a class="l" name="407" href="#407">407</a>    <a href="/source/s?defs=outputFile&amp;project=cern">outputFile</a>.<a href="/source/s?defs=Close&amp;project=cern">Close</a>()
<a class="l" name="408" href="#408">408</a>
<a class="l" name="409" href="#409">409</a>    <b>print</b> <span class="s">"=== wrote root file %s\n"</span> % <a href="/source/s?defs=outfname&amp;project=cern">outfname</a>
<a class="hl" name="410" href="#410">410</a>    <b>print</b> <span class="s">"=== TMVAClassification is done!\n"</span>
<a class="l" name="411" href="#411">411</a>
<a class="l" name="412" href="#412">412</a>    <span class="c"># open the GUI for the result macros</span>
<a class="l" name="413" href="#413">413</a>    <a class="d" href="#gROOT">gROOT</a>.<a href="/source/s?defs=ProcessLine&amp;project=cern">ProcessLine</a>( <span class="s">"TMVAGui(\"%s\")"</span> % <a href="/source/s?defs=outfname&amp;project=cern">outfname</a> )
<a class="l" name="414" href="#414">414</a>
<a class="l" name="415" href="#415">415</a>    <span class="c"># keep the ROOT thread running</span>
<a class="l" name="416" href="#416">416</a>    <a class="d" href="#gApplication">gApplication</a>.<a href="/source/s?defs=Run&amp;project=cern">Run</a>()
<a class="l" name="417" href="#417">417</a>
<a class="l" name="418" href="#418">418</a><span class="c"># ----------------------------------------------------------</span>
<a class="l" name="419" href="#419">419</a>
<a class="hl" name="420" href="#420">420</a><b>if</b> <a href="/source/s?defs=__name__&amp;project=cern">__name__</a> == <span class="s">"__main__"</span>:
<a class="l" name="421" href="#421">421</a>    <a class="d" href="#main">main</a>()
<a class="l" name="422" href="#422">422</a></pre>
</div>
    <div id="footer">
<p><a href="http://opengrok.github.com/OpenGrok/"
 title="Served by OpenGrok"><span id="fti"></span></a></p>
<p>
    <a href="http://www.rrzn.uni-hannover.de"><span id="partner_rrzn"></span></a>
    <a href="http://www.uni-hannover.de"><span id="partner_luh"></span></a>
</p>
<p><a href="http://www.metager.de/impressum.html">Impressum (legal notice)</a></p>
    
    </div>
    </div>
</div>
</body>
</html>

