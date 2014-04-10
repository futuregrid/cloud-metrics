class FGHighchartsTemplate:

    @staticmethod
    def get_datatable2pie():
        return '''
        /**
         * Create the data table
         */
        Highcharts.drawTable = function() {
            
            // user options
            var tableTop = 350,
                colWidth = 200,
                tableLeft = 60,
                rowHeight = 20,
                cellPadding = 2.5,
                valueDecimals = 1,
                valueSuffix = ' ';
                
            // internal variables
            var chart = this,
                series = chart.series,
                renderer = chart.renderer,
                cellLeft = tableLeft;

            var strLength = 33; 

            $.each(series, function(i, serie) {
                $.each(serie.data, function(row, point) {

                var trimmedString = point.name.length > strLength ? point.name.substring(0, strLength - 3) + " ..." : point.name.substring(0, strLength);
                    // Apply the cell text
                    renderer.text(
                            trimmedString,
                            cellLeft + cellPadding, 
                            tableTop + (row + 2) * rowHeight - cellPadding
                        )
                        .css({
                            fontWeight: 'bold'
                        })       
                        .add();
                    
                    // horizontal lines
                    if (row == 0) {
                        Highcharts.tableLine( // top
                            renderer,
                            tableLeft, 
                            tableTop + cellPadding,
                            cellLeft + colWidth, 
                            tableTop + cellPadding
                        );
                        Highcharts.tableLine( // bottom
                            renderer,
                            tableLeft, 
                            tableTop + (serie.data.length + 1) * rowHeight + cellPadding,
                            cellLeft + colWidth, 
                            tableTop + (serie.data.length + 1) * rowHeight + cellPadding
                        );
                    }
                    // horizontal line
                    Highcharts.tableLine(
                        renderer,
                        tableLeft, 
                        tableTop + row * rowHeight + rowHeight + cellPadding,
                        cellLeft + colWidth, 
                        tableTop + row * rowHeight + rowHeight + cellPadding
                    );
                        
                });

                cellLeft += colWidth;
                
                // Apply the cell text
                renderer.text(
                        serie.name,
                        cellLeft - cellPadding + colWidth, 
                        tableTop + rowHeight - cellPadding
                    )
                    .attr({
                        align: 'right'
                    })
                    .css({
                        fontWeight: 'bold'
                    })
                    .add();
                
                $.each(serie.data, function(row, point) {
                    
                    // Apply the cell text
                    renderer.text(
                            Highcharts.numberFormat(point.y, valueDecimals) + valueSuffix, 
                            cellLeft + colWidth - cellPadding, 
                            tableTop + (row + 2) * rowHeight - cellPadding
                        )
                        .attr({
                            align: 'right'
                        })
                        .add();
                    
                    // horizontal lines
                    if (row == 0) {
                        Highcharts.tableLine( // top
                            renderer,
                            tableLeft, 
                            tableTop + cellPadding,
                            cellLeft + colWidth, 
                            tableTop + cellPadding
                        );
                        Highcharts.tableLine( // bottom
                            renderer,
                            tableLeft, 
                            tableTop + (serie.data.length + 1) * rowHeight + cellPadding,
                            cellLeft + colWidth, 
                            tableTop + (serie.data.length + 1) * rowHeight + cellPadding
                        );
                    }
                    // horizontal line
                    Highcharts.tableLine(
                        renderer,
                        tableLeft, 
                        tableTop + row * rowHeight + rowHeight + cellPadding,
                        cellLeft + colWidth, 
                        tableTop + row * rowHeight + rowHeight + cellPadding
                    );
                        
                });
                
                // vertical lines        
                if (i == 0) { // left table border  
                    Highcharts.tableLine(
                        renderer,
                        tableLeft, 
                        tableTop + cellPadding,
                        tableLeft, 
                        tableTop + (serie.data.length + 1) * rowHeight + cellPadding
                    );
                }
                
                Highcharts.tableLine(
                    renderer,
                    cellLeft, 
                    tableTop + cellPadding,
                    cellLeft, 
                    tableTop + (serie.data.length + 1) * rowHeight + cellPadding
                );
                    
                if (i == series.length - 1) { // right table border    
         
                    Highcharts.tableLine(
                        renderer,
                        cellLeft + colWidth, 
                        tableTop + cellPadding,
                        cellLeft + colWidth, 
                        tableTop + (serie.data.length + 1) * rowHeight + cellPadding
                    );
                }
                
            });
            
                
        };

        /**
         * Draw a single line in the table
         */
        Highcharts.tableLine = function (renderer, x1, y1, x2, y2) {
            renderer.path(['M', x1, y1, 'L', x2, y2])
                .attr({
                    'stroke': 'silver',
                    'stroke-width': 1
                })
                .add();
        }
        '''
