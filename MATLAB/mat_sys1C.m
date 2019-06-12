clear
close all
filename = '/Users/AndreaTram/Desktop/AAU/CA4 Thesis/simulations/data_scripts/sys1setC.txt';
delimiter = ' ';
formatSpec = '%s%s%[^\n\r]';
fileID = fopen(filename,'r');
dataArray = textscan(fileID, formatSpec, 'Delimiter', delimiter, 'MultipleDelimsAsOne', true, 'TextType', 'string',  'ReturnOnError', false);
fclose(fileID);
raw = repmat({''},length(dataArray{1}),length(dataArray)-1);
for col=1:length(dataArray)-1
    raw(1:length(dataArray{col}),col) = mat2cell(dataArray{col}, ones(length(dataArray{col}), 1));
end
numericData = NaN(size(dataArray{1},1),size(dataArray,2));

for col=[1,2]
    % Converts text in the input cell array to numbers. Replaced non-numeric
    % text with NaN.
    rawData = dataArray{col};
    for row=1:size(rawData, 1)
        % Create a regular expression to detect and remove non-numeric prefixes and
        % suffixes.
        regexstr = '(?<prefix>.*?)(?<numbers>([-]*(\d+[\,]*)+[\.]{0,1}\d*[eEdD]{0,1}[-+]*\d*[i]{0,1})|([-]*(\d+[\,]*)*[\.]{1,1}\d+[eEdD]{0,1}[-+]*\d*[i]{0,1}))(?<suffix>.*)';
        try
            result = regexp(rawData(row), regexstr, 'names');
            numbers = result.numbers;
            
            % Detected commas in non-thousand locations.
            invalidThousandsSeparator = false;
            if numbers.contains(',')
                thousandsRegExp = '^\d+?(\,\d{3})*\.{0,1}\d*$';
                if isempty(regexp(numbers, thousandsRegExp, 'once'))
                    numbers = NaN;
                    invalidThousandsSeparator = true;
                end
            end
            % Convert numeric text to numbers.
            if ~invalidThousandsSeparator
                numbers = textscan(char(strrep(numbers, ',', '')), '%f');
                numericData(row, col) = numbers{1};
                raw{row, col} = numbers{1};
            end
        catch
            raw{row, col} = rawData{row};
        end
    end
end
sys1setC = cell2mat(raw);
clearvars filename delimiter formatSpec fileID dataArray ans raw col numericData rawData row regexstr result numbers invalidThousandsSeparator thousandsRegExp;


%% Analysis
%sys1 setting C 
%  A= np.array([[5, 2], [6 , 3]])      
%  b= np.array([[2],[12]])   
%  L = toeplitz([1,random.randint(1,10)])  
%  U = toeplitz([1,random.randint(1,10)])
%  ran= random.randint(1,501)

format long
x1=sys1setC(:,1);
x2=sys1setC(:,2);

e1=(-6)-x1;
e2=16-x2;

pe1=(e1./(-6))*100;
pe2=(e2./16)*100;


norm_1=(e1)./std(e1);
norm_2=(e2)./std(e2);

sorted_pe1=sort(pe1);
r_l2_5p1=sorted_pe1(26:end);
p95=r_l2_5p1(1:950);
lb1=min(p95);
ub1=max(p95);

sorted_pe2=sort(pe2);
r_l2_5p2=sorted_pe2(26:end);
p952=r_l2_5p2(1:950);
lb2=min(p952);
ub2=max(p952);

figure(1)
h1= histogram(pe1,'Normalization','probability'); hold on; 
ax = gca;
ax.YGrid = 'on';
ax.GridLineStyle = '-';
xlabel('Error deviation (%)')
ylabel('Probability')

h2= line([ lb1  lb1], [0 0.35], 'LineWidth',2, 'Color', 'k');

txt = '95 % lower bound \rightarrow';
text(lb1,0.275,txt,'HorizontalAlignment','right','FontSize',12)


h3=line([ub1 ub1], [0 0.35], 'LineWidth',2, 'Color', 'k');
txt = '\leftarrow 95 % upper bound';
text(ub1,0.275,txt,'FontSize',12)
legend([h1],{'e_1   system 1'})



figure(2)
h1= histogram(pe2,'Normalization','probability'); hold on; 
ax = gca;
ax.YGrid = 'on';
ax.GridLineStyle = '-';
xlabel('Error deviation (%)')
ylabel('Probability')

h2= line([ lb2  lb2], [0 0.35], 'LineWidth',2, 'Color', 'k');

txt = '95 % lower bound \rightarrow';
text(lb2,0.275,txt,'HorizontalAlignment','right','FontSize',12)


h3=line([ub2 ub2], [0 0.35], 'LineWidth',2, 'Color', 'k');
txt = '\leftarrow 95 % upper bound';
text(ub2,0.275,txt,'FontSize',12)
legend([h1],{'e_2'})
