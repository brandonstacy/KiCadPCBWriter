# python kicad scripting
# Brandon Stacy 
# Last Edit 10/24/2021
# can make two layer pcb antenna with vias

# import helper libraries
import numpy as np;

def KicadPCBWriter(filename, BtmE, TopE, Outlines, ViaArray, myText, TopMask, BtmMask, TopScreen, BtmScreen):
    FID = pcb_open(filename); # create pcb file
    pcb_general(FID); # create intial file headers
    pcb_netlist(FID, 0); # write nets to file

    for m in range(0,len(ViaArray)):
        pcb_via(FID,ViaArray[m][0],ViaArray[m][1],ViaArray[m][2],ViaArray[m][3],0); 
    for m in range(0,len(TopE)):
        pcb_filledPolygon(FID, TopE[m][0], TopE[m][1], 'F.Cu', 0);
    for m in range(0,len(BtmE)):
        pcb_filledPolygon(FID, BtmE[m][0], BtmE[m][1], 'B.Cu', 0);
    for m in range(0,len(Outlines)):
        pcb_outline(FID, Outlines[m][0], Outlines[m][1], 0.05)
    for m in range(0,len(TopMask)):
        pcb_filledPolygon(FID, TopMask[m][0], TopMask[m][1], 'F.Mask', 0);
    for m in range(0,len(BtmMask)):
        pcb_filledPolygon(FID, BtmMask[m][0], BtmMask[m][1], 'B.Mask', 0);
    for m in range(0,len(TopScreen)):
        pcb_filledPolygon(FID, TopScreen[m][0], TopScreen[m][1], 'F.SilkS', 0);
    for m in range(0,len(BtmScreen)):
        pcb_filledPolygon(FID, BtmScreen[m][0], BtmScreen[m][1], 'B.SilkS', 0);
    for m in range(0,len(myText)):
        pcb_text(FID,myText[m][0],myText[m][1],myText[m][2],myText[m][3],myText[m][4],myText[m][5],myText[m][6]);

    FID.write(  '  ) \n');
    pcb_close(FID);

def pcb_open(fname :str):
    file = open(fname,"w+");
    return file;

def pcb_close(FID):
    FID.close();

def pcb_via(FID,xpos,ypos,padsize,drillsize,netNO):
    PadSize = ' (size '+str(padsize)+')';
    DrillSize = ' (drill '+str(drillsize)+') ';
    pos = '(at '+str(xpos)+' '+str(ypos)+') '; 
    FID.write('  (via '+pos+PadSize+DrillSize+'(layers F.Cu B.Cu) (net '+str(netNO)+')) \n'); 

def pcb_text(FID,layer,x,y,sx,sy,thickness,text):
    layer = ' (layer '+layer +') \n';
    pos = ' (at ' +str(x) +' ' +str(y)+ ') '; 
    effect = '(effects (font (size '+str(sx)+' '+str(sy) +') (thickness '+str(thickness)+')))';
    FID.write('  (gr_text "' + text+'"'+ pos +layer +effect+ ') \n'); 

def pcb_filledPolygon(FID,Px,Py,myLayer,netNO):
    XYP = '';
    for m in range(0,len(Px)):
        XYP = XYP+'(xy '+str(Px[m])+ ' ' +str(Py[m])+ ') ';

    FID.write( '  (zone (net '+str(netNO)+') (net_name "") (layer '+myLayer+') (tstamp 5AB41BC6) (hatch edge 0.508) \n');
    FID.write(  '    (connect_pads (clearance 0.508)) \n');
    FID.write(  '    (min_thickness 0.254) \n');
    FID.write(  '    (fill yes (arc_segments 32) (thermal_gap 0.508) (thermal_bridge_width 0.508)) \n');
    FID.write(  '    (polygon \n');
    FID.write(  '      (pts \n');
    FID.write( '       ' +XYP+ ' \n');
    FID.write(  '      ) \n');
    FID.write(  '    ) \n');
    FID.write(  '    (filled_polygon \n');
    FID.write(  '      (pts \n');
    FID.write( '       ' +XYP +' \n');
    FID.write(  '      ) \n');
    FID.write(  '    ) \n');
    FID.write(  '  ) \n');

def pcb_outline(FID,Xoutline,Youtline,linewidth):
    tLY = ' (angle 90) (layer Edge.Cuts)'; 
    tLW = ' (width ' +str(linewidth) +')';
    for m in range(0,len(Xoutline)-1):
        tST  = ' (start ' +str(Xoutline[m])  + ' ' +str(Youtline[m])  + ')';
        tEND = ' (end '   +str(Xoutline[m+1])+ ' ' +str(Youtline[m+1])+ ')';
        FID.write('  (gr_line'+ tST+ tEND+ tLY+ tLW+ ') \n');    

def pcb_netlist(FID,netno):
    FID.write('  (net ' +str(netno) +' "") \n');
    FID.write( '  (net_class Default "default net class." \n');
    FID.write( '    (clearance 0.2) \n');
    FID.write( '    (trace_width 0.25) \n');
    FID.write( '    (via_dia 0.8) \n');
    FID.write( '    (via_drill 0.4) \n');
    FID.write( '    (uvia_dia 0.3) \n');
    FID.write( '    (uvia_drill 0.1) \n');
    FID.write( '  ) \n');
    FID.write( '   \n');
    FID.write( '   \n');

def pcb_general(FID):
    FID.write('(kicad_pcb (version 20171130) (host pcbnew "(5.1.5)-3") \n');
    FID.write('   \n');
    FID.write('  (general \n');
    FID.write('    (thickness 1.6) \n');
    FID.write('    (drawings 12) \n');
    FID.write('    (tracks 0) \n');
    FID.write('    (zones 0) \n');
    FID.write('    (modules 0) \n');
    FID.write('    (nets 1) \n');
    FID.write('  ) \n');
    FID.write('   \n');
    FID.write('  (page A4) \n');
    FID.write('  (layers \n');
    FID.write('    (0 F.Cu signal) \n');
    FID.write('    (31 B.Cu signal) \n');
    FID.write('    (32 B.Adhes user) \n');
    FID.write('    (33 F.Adhes user) \n');
    FID.write('    (34 B.Paste user) \n');
    FID.write('    (35 F.Paste user) \n');
    FID.write('    (36 B.SilkS user) \n');
    FID.write('    (37 F.SilkS user) \n');
    FID.write('    (38 B.Mask user) \n');
    FID.write('    (39 F.Mask user) \n');
    FID.write('    (40 Dwgs.User user) \n');
    FID.write('    (41 Cmts.User user) \n');
    FID.write('    (42 Eco1.User user) \n');
    FID.write('    (43 Eco2.User user) \n');
    FID.write('    (44 Edge.Cuts user) \n');
    FID.write('    (45 Margin user) \n');
    FID.write('    (46 B.CrtYd user) \n');
    FID.write('    (47 F.CrtYd user) \n');
    FID.write('    (48 B.Fab user) \n');
    FID.write('    (49 F.Fab user) \n');
    FID.write('  ) \n');
    FID.write('   \n');
    FID.write('  (setup \n');
    FID.write('    (last_trace_width 0.25) \n');
    FID.write('    (trace_clearance 0.2) \n');
    FID.write('    (zone_clearance 0.508) \n');
    FID.write('    (zone_45_only no) \n');
    FID.write('    (trace_min 0.2) \n');
    FID.write('    (segment_width 0.2) \n');
    FID.write('    (edge_width 0.05) \n');
    FID.write('    (via_size 0.4) \n');
    FID.write('    (via_drill 0.3) \n');
    FID.write('    (via_min_size 0.4) \n');
    FID.write('    (via_min_drill 0.3) \n');
    FID.write('    (uvia_size 0.3) \n');
    FID.write('    (uvia_drill 0.1) \n');
    FID.write('    (uvias_allowed no) \n');
    FID.write('    (uvia_min_size 0.2) \n');
    FID.write('    (uvia_min_drill 0.1) \n');
    FID.write('    (pcb_text_width 0.3) \n');
    FID.write('    (pcb_text_size 1.5 1.5) \n');
    FID.write('    (mod_edge_width 0.12) \n');
    FID.write('    (mod_text_size 1 1) \n');
    FID.write('    (mod_text_width 0.15) \n');
    FID.write('    (pad_size 1.524 1.524) \n');
    FID.write('    (pad_drill 0.762) \n');
    FID.write('    (pad_to_mask_clearance 0.051) \n');
    FID.write('    (solder_mask_min_width 0.25) \n');
    FID.write('    (aux_axis_origin 0 0) \n');
    FID.write('    (visible_elements 7FFFFFFF) \n');
    FID.write('    (pcbplotparams \n');
    FID.write('      (layerselection 0x010fc_ffffffff) \n');
    FID.write('      (usegerberextensions false) \n');
    FID.write('      (usegerberattributes false) \n');
    FID.write('      (usegerberadvancedattributes false) \n');
    FID.write('      (creategerberjobfile false) \n');
    FID.write('      (excludeedgelayer true) \n');
    FID.write('      (linewidth 0.100000) \n');
    FID.write('      (plotframeref false) \n');
    FID.write('      (viasonmask false) \n');
    FID.write('      (mode 1) \n');
    FID.write('      (useauxorigin false) \n');
    FID.write('      (hpglpennumber 1) \n');
    FID.write('      (hpglpenspeed 20) \n');
    FID.write('      (hpglpendiameter 15.000000) \n');
    FID.write('      (psnegative false) \n');
    FID.write('      (psa4output false) \n');
    FID.write('      (plotreference true) \n');
    FID.write('      (plotvalue true) \n');
    FID.write('      (plotinvisibletext false) \n');
    FID.write('      (padsonsilk false) \n');
    FID.write('      (subtractmaskfromsilk false) \n');
    FID.write('      (outputformat 1) \n');
    FID.write('      (mirror false) \n');
    FID.write('      (drillshape 1) \n');
    FID.write('      (scaleselection 1) \n');
    FID.write('      (outputdirectory "") \n');
    FID.write('    ) \n');
    FID.write('  ) \n');
    FID.write('   \n');
    FID.write('   \n');

# comment out main when using as module
def main():
    xoffset = 100; # mm
    yoffset = 25; # mm
    Frequency = 2; # GHz

    filename = str(Frequency)+"GHz_PatchPy.kicad_pcb";

    # Patch Parameters
    Wpatch = 46;
    Lpatch = 35;

    # Substrate and ground Parameters
    SubstrateLength = 100;
    SubstrateWidth = 100;

    # Feed Parameters
    W0 = 2.29;
    W1 = 2.4;
    CutoutLength = 10; # cutout in patch
    FeedGap = 1;

    # SMA Edge Connector Parameters
    ConCutoutWidth = 2.92;
    ConCutoutLength = .71;
    ConPadLength = 5.84;
    ConPadWidth = 4.83;
    ConCutoutOffset = .51;
    ConSignalSpace = 2.03;

    # Via Parameters
    Padsize = .3;
    Drillsize = .15;

    # patch 
    PatchX = [-W0/2, -W0/2, -W1/2, -W1/2, -W1/2-FeedGap, -W1/2-FeedGap, -Wpatch/2, -Wpatch/2, Wpatch/2,
    Wpatch/2, W1/2+FeedGap, W1/2+FeedGap, W1/2, W1/2, W0/2, W0/2, -W0/2];
    PatchY = [0, ConPadLength, ConPadLength, SubstrateLength/2-Lpatch/2+CutoutLength, SubstrateLength/2-Lpatch/2+CutoutLength, SubstrateLength/2-Lpatch/2, 
        SubstrateLength/2-Lpatch/2, SubstrateLength/2+Lpatch/2, SubstrateLength/2+Lpatch/2, SubstrateLength/2-Lpatch/2, 
        SubstrateLength/2-Lpatch/2, SubstrateLength/2-Lpatch/2+CutoutLength, SubstrateLength/2-Lpatch/2+CutoutLength, 
        ConPadLength, ConPadLength, 0, 0];

    # ground and substrate 
    GroundX = [-SubstrateWidth/2, -SubstrateWidth/2, SubstrateWidth/2, SubstrateWidth/2,
    ConSignalSpace+ConCutoutOffset+ConCutoutWidth, ConSignalSpace+ConCutoutOffset+ConCutoutWidth, 
    ConSignalSpace+ConCutoutOffset, ConSignalSpace+ConCutoutOffset, -ConSignalSpace-ConCutoutOffset,
    -ConSignalSpace-ConCutoutOffset, -ConSignalSpace-ConCutoutOffset-ConCutoutWidth, -ConSignalSpace-ConCutoutOffset-ConCutoutWidth,-SubstrateWidth/2];
    GroundY = [0, SubstrateLength, SubstrateLength, 0, 0, ConCutoutLength, ConCutoutLength, 0, 0, ConCutoutLength, ConCutoutLength, 0, 0];

    # Connector
    ConPadLeftX = [-ConSignalSpace, -ConSignalSpace-ConCutoutOffset, -ConSignalSpace-ConCutoutOffset,
        -ConSignalSpace-ConCutoutOffset-ConCutoutWidth, -ConSignalSpace-ConCutoutOffset-ConCutoutWidth,
        -ConPadWidth-ConSignalSpace, -ConPadWidth-ConSignalSpace, -ConSignalSpace, -ConSignalSpace];
    ConPadRightX = np.multiply(ConPadLeftX,-1)
    ConPadY = [0,0, ConCutoutLength, ConCutoutLength, 0, 0, ConPadLength, ConPadLength, 0];

    # Via Locations
    ViasX = [-ConPadWidth/2-ConSignalSpace, ConPadWidth/2+ConSignalSpace];
    ViasY = [ConPadLength*3/4, ConPadLength*3/4];

    # add x and y-offset
    PatchX = np.array(PatchX);
    PatchY = np.array(PatchY);
    ConPadLeftX = np.array(ConPadLeftX);
    ConPadRightX = np.array(ConPadRightX);
    ConPadY = np.array(ConPadY);
    GroundX = np.array(GroundX);
    GroundY = np.array(GroundY);
    ViasX = np.array(ViasX);
    ViasY = np.array(ViasY);

    PatchX = PatchX+xoffset;
    PatchY = PatchY+yoffset;
    ConPadLeftX = ConPadLeftX+xoffset;
    ConPadRightX = ConPadRightX+xoffset;
    ConPadY = ConPadY+yoffset;
    GroundX = GroundX+xoffset;
    GroundY = GroundY+yoffset;
    ViasX = ViasX+xoffset;
    ViasY = ViasY+yoffset;

    # making final arrays to be passed into pcb writer
    Vias = [];
    for i in range(0,len(ViasX)):
        temp_vias = [];
        temp_vias.append(ViasX[i]);
        temp_vias.append(ViasY[i]);
        temp_vias.append(Padsize);
        temp_vias.append(Drillsize);
        Vias.append(temp_vias);

    BtmE = [[GroundX,GroundY]];
    TopE = [[PatchX,PatchY],[ConPadLeftX,ConPadY],[ConPadRightX,ConPadY]];
    myText = [['F.Cu',0,0,1.5,1.5,.3,"Brandon S."]];

    # KicadPCBWriter(filename, BtmE, TopE, Outlines, ViaArray, myText, TopMask, BtmMask, TopScreen, BtmScreen): # pcb writer 
    KicadPCBWriter(filename,BtmE,TopE,BtmE,Vias,myText,[],[],[],BtmE);

if __name__ == "__main__":
    main();