(function (nx) {
    /**
     * NeXt UI based application
     */
    // Initialize topology
    var topo = new nx.graphic.Topology({
        // View dimensions
        width: 1200,
        height: 700,
        // Dataprocessor is responsible for spreading 
        // the Nodes across the view.
        // 'force' data processor spreads the Nodes so
        // they would be as distant from each other
        // as possible. Follow social distancing and stay healthy.
        // 'quick' dataprocessor picks random positions
        // for the Nodes.
        dataProcessor: 'force',
        // Node and Link identity key attribute name
        identityKey: 'id',
        // Node settings
        nodeConfig: {
            label: 'model.name',
            iconType:'model.icon',
        },
        // Link settings
        linkConfig: {
            // Display Links as curves in case of 
            // multiple links between Node Pairs.
            // Set to 'parallel' to use parallel links.
            linkType: 'curve',
        },
        // Display Node icon. Displays a dot if set to 'false'.
        showIcon: true,
    });

    var Shell = nx.define(nx.ui.Application, {
        methods: {
            start: function () {
                // Read topology data from variable
                topo.data(topologyData);
                // Attach it to the document
                topo.attach(this);
            }
        }
    });

    // Create an application instance
    var shell = new Shell();
    // Run the application
    shell.start();
})(nx);