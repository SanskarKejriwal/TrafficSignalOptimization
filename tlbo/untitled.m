clc
close
commandwindow

import = @importfile;
[funEval0, best0, avg0] = import("run0.csv");
[funEval1, best1, avg1] = import("run1.csv");
[funEval2, best2, avg2] = import("run2.csv");
[funEval3, best3, avg3] = import("run3.csv");
[funEval4, best4, avg4] = import("run4.csv");

funEvalUpto = 2500;
funEval(2200)
avgUpto = 100;
funEval0 = funEval0(1:funEvalUpto);
funEval1 = funEval1(1:funEvalUpto);
funEval2 = funEval2(1:funEvalUpto);
funEval3 = funEval3(1:funEvalUpto);
funEval4 = funEval4(1:funEvalUpto);
avg0 = avg0(1:avgUpto);
avg1 = avg1(1:avgUpto);
avg2 = avg2(1:avgUpto);
avg3 = avg3(1:avgUpto);
avg4 = avg4(1:avgUpto);

funEval = (funEval0 + funEval1 + funEval2 + funEval3 + funEval4) / 5;
avg = (avg0 + avg1 + avg2 + avg3 + avg4) / 5;

plt = @plotNew
size(funEval4)

funEval = funEval(1:funEvalUpto);
avg = avg(1:avgUpto);

plt(log10(abs(funEval)),'Log_{10} |Best Fitness| vs Function Evaluations','Function Evaluations','Log_{10} |Best Fitness|')

plt(log10(abs(avg)),'Log_{10} |Average Fitness| vs Iterations','Iterations','Log_{10} |Average Fitness|')

function plotNew(a,titleString,xax,yax)
    plot(a)
    title(titleString);
    xlabel(xax);
    ylabel(yax);
    hold on
    [~,aI] = unique(a,'first');
    %plot(aI,a(aI),'r*')
    hold off
    figure
end