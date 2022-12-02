clc
close
commandwindow

import = @importfile;
[funEval0, best0, avg0] = import("run0.csv");
[funEval1, best1, avg1] = import("run1.csv");
[funEval2, best2, avg2] = import("run2.csv");
[funEval3, best3, avg3] = import("run3.csv");
[funEval4, best4, avg4] = import("run4.csv");

funEval0(1000)
funEval1(1000)
funEval2(1000)
funEval3(1000)
funEval4(1000)

funEval = (funEval0 + funEval1 + funEval2 + funEval3 + funEval4) / 5;
avg = (avg0 + avg1 + avg2 + avg3 + avg4) / 5;

plt = @plotNew
size(funEval4)
funEvalUpto = 120;
funEval = funEval(1:funEvalUpto);

avgUpto = 20;
avg = avg(1:avgUpto);

plt(log10(abs(funEval)),'Log_{10} |Best Fitness| vs Function Evaluations','Function Evaluations','Log_{10} |Best Fitness|')
plt(funEval,'Test','Function Evaluations','Log_{10} |Best Fitness|')

plt(log10(abs(avg)),'Log_{10} |Average Fitness| vs Iterations','Iterations','Log_{10} |Average Fitness|')

function plotNew(a,titleString,xax,yax)
    plot(a)
    title(titleString);
    xlabel(xax);
    ylabel(yax);
    hold on
    [~,aI] = unique(a,'first');
    plot(aI,a(aI),'r*')
    hold off
    figure
end