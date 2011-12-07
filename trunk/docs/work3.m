function [ output_args ] = work3( input_args )
%WORK Summary of this function goes here
%   Detailed explanation goes here

m = [0.039153357718971347, 0.044015967462529185, 0.058857258875269755]


figure;

bar(m,'grouped');
set(gca,'XTickLabel',['rbf_1e2'; 'rbf_1e3'; 'rbf_1e4'])
title('m')


end





