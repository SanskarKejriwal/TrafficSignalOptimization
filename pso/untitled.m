clc
close
commandwindow

import = @importfile;
[funEval0, best0, avg0] = import("run0.csv");
[funEval1, best1, avg1] = import("run1.csv");
[funEval2, best2, avg2] = import("run2.csv");
[funEval3, best3, avg3] = import("run3.csv");
[funEval4, best4, avg4] = import("run4.csv");

a1=max(funEval0)
a2=max(funEval1)
a3=max(funEval2)
a4=max(funEval3)
a5=max(funEval4)



size(funEval4)

funEval = (funEval0 + funEval1 + funEval2 + funEval3 + funEval4) / 5;
avg = (avg0 + avg1 + avg2 + avg3 + avg4) / 5;

plt = @plotNew

funEvalUpto = 30;
funEval = funEval(1:funEvalUpto);

avgUpto = 100;
avg(end)
avg = avg(1:avgUpto);

plt(funEval,'Log_{10} |Best Fitness| vs Function Evaluations','Function Evaluations','Log_{10} |Best Fitness|','r*')

plt(avg,'Log_{10} |Average Fitness| vs Iterations','Iterations','Log_{10} |Average Fitness|','')

function plotNew(a,titleString,xax,yax,style)
    plot(a)
    title(titleString);
    xlabel(xax);
    ylabel(yax);
    hold on
    [~,aI] = unique(a,'first');
    if style == 'r*'
        plot(aI,a(aI),'r*')
    elseif style == ''
        plot(aI,a(aI))
    end
    hold off
    figure
end