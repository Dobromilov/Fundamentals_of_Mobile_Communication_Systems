clear; clc;

fs = 44100;
bpm = 180;
beat = 60 / bpm;              % длительность четверти
barLength = 3 * beat;          % 6/8 = 3 четверти в такте

% Каждая строка: {нота или аккорд в MIDI, длительность в четвертях}
A = {62,1; 62,.5; 62,1; 62,.5};
B = {62,1; 62,.5; 62,.5; 62,.5; 62,.5};

RH = cell(14,1);
RH{1}=A; RH{2}=B; RH{3}=A; RH{4}=B; RH{5}=A;
RH{6}  = {62,1; 62,.5; [],.5; 57,.5; 60,.5};
RH{7}  = {[53 57 62],1; [53 57 62],1; 62,.5; 64,.5};
RH{8}  = {[58 62 65],1; [58 62 65],1; 65,.5; 67,.5};
RH{9}  = {[55 60 64],1; [55 60 64],1; 62,.5; 60,.5};
RH{10} = {60,.5; [53 57 60],1; [],.5; 57,.5; 60,.5};
RH{11} = {[53 57 60],1; [53 57 60],1; 62,.5; 64,.5};
RH{12} = {[57 60 65],1; [57 60 65],1; 65,.5; 67,.5};
RH{13} = {[55 60 64],1; [55 60 64],1; 62,.5; 60,.5};
RH{14} = {[53 57 60],1; [],1; 57,.5; 60,.5};

% Бас начинается с пятого такта
bass = [38 38 38 34 31 36 34 29 36 38]; % D2, Bb1 и т. д.

N = round(14 * barLength * fs);
fragment = zeros(1,N);

for bar = 1:14
    events = RH{bar};
    position = (bar-1) * barLength;

    for e = 1:size(events,1)
        notes = events{e,1};
        duration = events{e,2} * beat;

        if ~isempty(notes)
            n = round(duration * fs);
            t = (0:n-1) / fs;
            env = min(1,t/0.012) .* min(1,(duration-t)/0.06) ...
                  .* exp(-0.35*t);

            for midi = notes
                f = 440 * 2^((midi-69)/12);
                tone = env .* (sin(2*pi*f*t) ...
                            + 0.28*sin(4*pi*f*t) ...
                            + 0.10*sin(6*pi*f*t));
                idx = round(position*fs) + (1:n);
                fragment(idx) = fragment(idx) + 0.35*tone;
            end
        end

        position = position + duration;
    end
end

% Бас: две доли на каждый такт, начиная с пятого
for bar = 5:14
    root = bass(bar-4);
    for half = 0:1
        position = (bar-1)*barLength + half*1.5*beat;
        duration = 1.3*beat;
        n = round(duration*fs);
        t = (0:n-1)/fs;
        env = min(1,t/0.015) .* exp(-2.2*t);

        f1 = 440 * 2^((root-69)/12);
        f2 = 2*f1;
        tone = env .* (sin(2*pi*f1*t) + 0.35*sin(2*pi*f2*t));

        idx = round(position*fs) + (1:n);
        fragment(idx) = fragment(idx) + 0.22*tone;
    end
end

% Повторяем весь фрагмент дважды
audio = fragment;
audio = 0.9 * audio / max(abs(audio));
sound(audio,fs);