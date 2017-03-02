package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"net/http"
	"time"

	"gopkg.in/raintank/schema.v1"
)

var url = "https://<your-subdomain>.hosted-metrics.grafana.net/metrics"
var apiKey = "<your api key from grafana.net -- should be editor role>"

// createPoint creates a datapoint, i.e. a MetricData structure, and makes sure the id is set.
func createPoint(name string, interval int, val float64, time int64) *schema.MetricData {
	md := schema.MetricData{
		Name:     name,       // in graphite style format. should be same as Metric field below (used for partitioning, schema matching, indexing)
		Metric:   name,       // in graphite style format. should be same as Name field above (used to generate Id)
		Interval: interval,   // the resolution of the metric
		Value:    val,        // float64 value
		Unit:     "",         // not needed or used yet
		Time:     time,       // unix timestamp in seconds
		Mtype:    "gauge",    // not used yet. but should be one of gauge rate count counter timestamp
		Tags:     []string{}, // not needed or used yet. can be single words or key:value pairs
	}
	md.SetId()
	return &md
}

func main() {
	// create an array of schema.MetricData structures which will hold our points
	// we will add 10 example points
	metrics := schema.MetricDataArray{}

	now := time.Now().Unix()

	metrics = append(metrics, createPoint("my.test.metric", 10, 0.23, now-90))
	metrics = append(metrics, createPoint("my.test.metric", 10, 1.23, now-80))
	metrics = append(metrics, createPoint("my.test.metric", 10, 2.23, now-70))
	metrics = append(metrics, createPoint("my.test.metric", 10, 3.23, now-60))
	metrics = append(metrics, createPoint("my.test.metric", 10, 4.23, now-50))
	metrics = append(metrics, createPoint("my.test.metric", 10, 5.23, now-40))
	metrics = append(metrics, createPoint("my.test.metric", 10, 6.23, now-30))
	metrics = append(metrics, createPoint("my.test.metric", 10, 7.23, now-20))
	metrics = append(metrics, createPoint("my.test.metric", 10, 8.23, now-10))
	metrics = append(metrics, createPoint("my.test.metric", 10, 9.23, now))

	// encode as json
	data, err := json.Marshal(metrics)
	if err != nil {
		panic(err)
	}

	client := &http.Client{}

	req, err := http.NewRequest("POST", url, bytes.NewBuffer(data))
	if err != nil {
		panic(err)
	}

	req.Header.Add("Authorization", "Bearer "+apiKey)
	req.Header.Add("Content-Type", "application/json")
	resp, err := client.Do(req)
	if err != nil {
		panic(err)
	}
	buf := make([]byte, 4096)
	n, err := resp.Body.Read(buf)
	fmt.Println(resp.StatusCode, resp.Status)
	fmt.Println(string(buf[:n]))
}
