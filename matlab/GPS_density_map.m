function GPS_density_map()

    
    plot_one_day('../data/2012-10-29.csv');
    
    plot_one_day('../data/2012-12-25.csv');
    
    
    plot_one_day('../data/2012-12-08.csv');
    
    plot_one_day('../data/2012-12-10.csv');



    function plot_one_day( fname )
        
        gpsNYC = importdata(fname);

        pickups = gpsNYC(:,1:2);
        pickups = pickups(pickups(:,1) < -73.92 & pickups(:,1) > -74.03, :);
        pickups = pickups(pickups(:,2) > 40.68 & pickups(:,2) < 40.86,:);


        [h, c] = hist3(pickups, [200, 200]);   % put GPS into n-by-n bins
        hn = h';
%         hn(hn==0) = NaN;


        figure()

%         cmap = [
%             128, 255, 255;
%             191, 255, 128;
%             255, 255, 0;
%             255, 223, 0;
%             255, 191, 0;
%             255, 159, 0;
%             255, 128, 0;
%             255, 96, 0;
%             255, 64, 0;
%             255, 32, 0;
%             255, 0, 0];
%         colormap(cmap/255);

        surf(c{1}, c{2}, hn, 'edgecolor', 'none');
        view(0, 90);
        box on;
        grid off


        colorbar()
        axis([-74.03, -73.92, 40.68, 40.86]);
    end


end