export default {
    async fetch(request, env) {
        const tasks = [];
        
        // prompt - simple completion style input
        let simple = {
            prompt: "Generate a captivating story set in the world of SteamSpire, a Victorian-era Steampunk city-builder game. In this narrative, players take on the role of a city planner managing a burgeoning city. They must strategically build industrial zones to increase their steam count, commercial zones to boost their gear count, and residential zones to grow the population. Highlight the interaction between commercial and residential zones, explaining how the adjacency influences gear production. Include the risks and rewards of investing in military zones, the mechanics of claiming land through invasion versus purchase, and the consequences of failure. Emphasize the time limit players choose for their playthrough and the ultimate goal of building the most prosperous city. Finally, describe how players will be graded on their achievements at the end. The story should inspire excitement and strategy, illustrating the challenges and triumphs of city-building in a steampunk world."
        };
        let response = await env.AI.run('@cf/meta/llama-3-8b-instruct', simple);
        tasks.push({ inputs: simple, response });
    
        return Response.json(tasks);
    }
};