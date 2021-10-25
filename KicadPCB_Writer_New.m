function KicadPCB_Writer(filename, BtmE, TopE, Outlines, ViaArray, myText, TopMask, BtmMask, TopScreen, BtmScreen) 


FID = pcb_open(filename);
pcb_general(FID);
pcb_netlist(FID, 0); 

for m = 1:length(ViaArray)
    pcb_via(FID, ViaArray(m), 0); 
end
for m = 1:length(TopE)
    pcb_filledPolygon(FID, TopE(m).x, TopE(m).y, 'F.Cu', 0);
end
for m = 1:length(BtmE)
    pcb_filledPolygon(FID, BtmE(m).x, BtmE(m).y, 'B.Cu', 0);
end
for m = 1:length(Outlines)
    FID = pcb_outline(FID, Outlines(m).x, Outlines(m).y, 0.02);      
end
for m = 1:length(myText)
    FID = pcb_text(FID, myText(m));
end
for m = 1:length(TopMask)
    pcb_filledPolygon(FID, TopMask(m).x, TopMask(m).y, 'F.Mask', 0);
end
for m = 1:length(BtmMask)
    pcb_filledPolygon(FID, BtmMask(m).x, BtmMask(m).y, 'B.Mask', 0);
end
for m = 1:length(TopScreen)
    pcb_filledPolygon(FID, TopScreen.x, TopScreen(m).y, 'F.SilkS', 0);
end
for m = 1:length(BtmScreen)
    pcb_filledPolygon(FID, BtmScreen(m).x, BtmScreen(m).y, 'B.SilkS', 0);
end
%++++++++++++++++++++++++++++
fprintf(FID,') \n');
pcb_close(FID); 

end

%=========================================================================
%=========================================================================
%=========================================================================
function FID = pcb_filledPolygon(FID, Px, Py, myLayer, netNO)

XYP = '';
for m = 1:length(Px)
    XYP = [XYP '(xy ' num2str(Px(m)) ' ' num2str(Py(m)) ') '];
end
fprintf(FID, ['  (zone (net ' num2str(netNO) ') (net_name "") (layer ' myLayer ') (tstamp 5AB41BC6) (hatch edge 0.508) \n']);
fprintf(FID,  '    (connect_pads (clearance 0.508)) \n');
fprintf(FID,  '    (min_thickness 0.254) \n');
fprintf(FID,  '    (fill yes (arc_segments 32) (thermal_gap 0.508) (thermal_bridge_width 0.508)) \n');
fprintf(FID,  '    (polygon \n');
fprintf(FID,  '      (pts \n');
fprintf(FID, ['       ' XYP ' \n']);
fprintf(FID,  '      ) \n');
fprintf(FID,  '    ) \n');

fprintf(FID,  '    (filled_polygon \n');
fprintf(FID,  '      (pts \n');
fprintf(FID, ['       ' XYP ' \n']);
fprintf(FID,  '      ) \n');
fprintf(FID,  '    ) \n');
fprintf(FID,  '  ) \n');

end
%=========================================================================
function FID = pcb_polygon(FID, Px, Py, myLayer, netNO)

XYP = '';
for m = 1:length(Px)
    XYP = [XYP '(xy ' num2str(Px(m)) ' ' num2str(Py(m)) ') '];
end

fprintf(FID, ['  (zone (net ' num2str(netNO) ') (net_name "") (layer ' myLayer ') \n']);
fprintf(FID,  '    (polygon \n');
fprintf(FID,  '      (pts \n');
fprintf(FID, ['       ' XYP ' \n']);
fprintf(FID,  '      ) \n');
fprintf(FID,  '    ) \n');
fprintf(FID,  '  ) \n');
fprintf(FID, '   \n');

end
%=========================================================================
function FID = pcb_via(FID, Via, netNO)

PadSize = [' (size ' num2str(Via.padsize) ')'];
DrillSize = [' (drill ' num2str(Via.drillsize) ') '];
pos = ['(at ' num2str(Via.x) ' ' num2str(Via.y) ') ']; 

fprintf(FID, ['  (via ' pos PadSize DrillSize '(layers F.Cu B.Cu) (net ' num2str(netNO) ')) \n']); 

end
%=========================================================================
function FID = pcb_text(FID, myText)

layer = [' (layer ' myText.layer ') '];
pos = [' (at ' num2str(myText.x) ' ' num2str(myText.y) ') ']; 
effect = ['(effects (font (size ' num2str(myText.sx) ' ' num2str(myText.sy) ') (thickness ' num2str(myText.thickness) ')))'];

fprintf(FID, ['  (gr_text '  myText.text pos layer effect ') \n']); 
  
 end


%=========================================================================
function FID = pcb_outline(FID, Xoutline, Youtline, linewidth)

tLY = ' (angle 90) (layer Edge.Cuts)'; 
tLW = [' (width ' num2str(linewidth) ')'];
for m = 1:length(Xoutline)-1
    tST  = [' (start ' num2str(Xoutline(m))   ' ' num2str(Youtline(m))   ')'];
    tEND = [' (end '   num2str(Xoutline(m+1)) ' ' num2str(Youtline(m+1)) ')'];
    fprintf(FID, ['  (gr_line' tST tEND tLY tLW ') \n']);    
end

end
%=========================================================================
function FID = pcb_netlist(FID, netNO)

fprintf(FID,['  (net ' num2str(netNO) ' "") \n']);
fprintf(FID, '  (net_class Default "default net class." \n');
fprintf(FID, '    (clearance 0.2) \n');
fprintf(FID, '    (trace_width 0.25) \n');
fprintf(FID, '    (via_dia 0.8) \n');
fprintf(FID, '    (via_drill 0.4) \n');
fprintf(FID, '    (uvia_dia 0.3) \n');
fprintf(FID, '    (uvia_drill 0.1) \n');
fprintf(FID, '  ) \n');
fprintf(FID, '   \n');
fprintf(FID, '   \n');

end
%=========================================================================
function FID = pcb_general(FID); 

fprintf(FID,'(kicad_pcb (version 20171130) (host pcbnew "(5.1.5)-3") \n');
fprintf(FID,'   \n');
fprintf(FID,'  (general \n');
% fprintf(FID,'    (links 0) \n');
% fprintf(FID,'    (no_connects 0) \n');
% fprintf(FID,'    (area 125.6 37.9082 128.700001 40.7442) \n');
fprintf(FID,'    (thickness 1.6) \n');
fprintf(FID,'    (drawings 12) \n');
fprintf(FID,'    (tracks 0) \n');
fprintf(FID,'    (zones 0) \n');
fprintf(FID,'    (modules 0) \n');
fprintf(FID,'    (nets 1) \n');
fprintf(FID,'  ) \n');
fprintf(FID,'   \n');

fprintf(FID,'  (page A4) \n');
fprintf(FID,'  (layers \n');
fprintf(FID,'    (0 F.Cu signal) \n');
fprintf(FID,'    (31 B.Cu signal) \n');
fprintf(FID,'    (32 B.Adhes user) \n');
fprintf(FID,'    (33 F.Adhes user) \n');
fprintf(FID,'    (34 B.Paste user) \n');
fprintf(FID,'    (35 F.Paste user) \n');
fprintf(FID,'    (36 B.SilkS user) \n');
fprintf(FID,'    (37 F.SilkS user) \n');
fprintf(FID,'    (38 B.Mask user) \n');
fprintf(FID,'    (39 F.Mask user) \n');
fprintf(FID,'    (40 Dwgs.User user) \n');
fprintf(FID,'    (41 Cmts.User user) \n');
fprintf(FID,'    (42 Eco1.User user) \n');
fprintf(FID,'    (43 Eco2.User user) \n');
fprintf(FID,'    (44 Edge.Cuts user) \n');
fprintf(FID,'    (45 Margin user) \n');
fprintf(FID,'    (46 B.CrtYd user) \n');
fprintf(FID,'    (47 F.CrtYd user) \n');
fprintf(FID,'    (48 B.Fab user) \n');
fprintf(FID,'    (49 F.Fab user) \n');
fprintf(FID,'  ) \n');
fprintf(FID,'   \n');
  
fprintf(FID,'  (setup \n');
fprintf(FID,'    (last_trace_width 0.25) \n');
fprintf(FID,'    (trace_clearance 0.2) \n');
fprintf(FID,'    (zone_clearance 0.508) \n');
fprintf(FID,'    (zone_45_only no) \n');
fprintf(FID,'    (trace_min 0.2) \n');
fprintf(FID,'    (segment_width 0.2) \n');
fprintf(FID,'    (edge_width 0.05) \n');
fprintf(FID,'    (via_size 0.4) \n');
fprintf(FID,'    (via_drill 0.3) \n');
fprintf(FID,'    (via_min_size 0.4) \n');
fprintf(FID,'    (via_min_drill 0.3) \n');
fprintf(FID,'    (uvia_size 0.3) \n');
fprintf(FID,'    (uvia_drill 0.1) \n');
fprintf(FID,'    (uvias_allowed no) \n');
fprintf(FID,'    (uvia_min_size 0.2) \n');
fprintf(FID,'    (uvia_min_drill 0.1) \n');
fprintf(FID,'    (pcb_text_width 0.3) \n');
fprintf(FID,'    (pcb_text_size 1.5 1.5) \n');
fprintf(FID,'    (mod_edge_width 0.12) \n');
fprintf(FID,'    (mod_text_size 1 1) \n');
fprintf(FID,'    (mod_text_width 0.15) \n');
fprintf(FID,'    (pad_size 1.524 1.524) \n');
fprintf(FID,'    (pad_drill 0.762) \n');
fprintf(FID,'    (pad_to_mask_clearance 0.051) \n');
fprintf(FID,'    (solder_mask_min_width 0.25) \n');
fprintf(FID,'    (aux_axis_origin 0 0) \n');
fprintf(FID,'    (visible_elements 7FFFFFFF) \n');
fprintf(FID,'    (pcbplotparams \n');
fprintf(FID,'      (layerselection 0x010fc_ffffffff) \n');
fprintf(FID,'      (usegerberextensions false) \n');
fprintf(FID,'      (usegerberattributes false) \n');
fprintf(FID,'      (usegerberadvancedattributes false) \n');
fprintf(FID,'      (creategerberjobfile false) \n');
fprintf(FID,'      (excludeedgelayer true) \n');
fprintf(FID,'      (linewidth 0.100000) \n');
fprintf(FID,'      (plotframeref false) \n');
fprintf(FID,'      (viasonmask false) \n');
fprintf(FID,'      (mode 1) \n');
fprintf(FID,'      (useauxorigin false) \n');
fprintf(FID,'      (hpglpennumber 1) \n');
fprintf(FID,'      (hpglpenspeed 20) \n');
fprintf(FID,'      (hpglpendiameter 15.000000) \n');
% fprintf(FID,'      (hpglpenoverlay 2) \n');
fprintf(FID,'      (psnegative false) \n');
fprintf(FID,'      (psa4output false) \n');
fprintf(FID,'      (plotreference true) \n');
fprintf(FID,'      (plotvalue true) \n');
fprintf(FID,'      (plotinvisibletext false) \n');
fprintf(FID,'      (padsonsilk false) \n');
fprintf(FID,'      (subtractmaskfromsilk false) \n');
fprintf(FID,'      (outputformat 1) \n');
fprintf(FID,'      (mirror false) \n');
fprintf(FID,'      (drillshape 1) \n');
fprintf(FID,'      (scaleselection 1) \n');
fprintf(FID,'      (outputdirectory "") \n');
fprintf(FID,'    ) \n');
fprintf(FID,'  ) \n');
fprintf(FID,'   \n');
fprintf(FID,'   \n');

end

%=========================================================================
function FID = pcb_open(fname) 

try   
    FID = fopen(fname,'w');
catch exception
    if FID >= 0
        fclose(FID);
    end
    rethrow(exception);
end
end


%=========================================================================
function pcb_close(FID)

try
  fprintf(FID,' \n');
  fclose(FID);
catch exception
  if FID >= 0
    fclose(FID);
  end
  rethrow(exception);
end
end