# City of Oklahoma City

Support for waste collection schedules in the City of Oklahoma City, retrieved from the public `okc.schizo.dev` feed.

## Configuration via configuration.yaml

```yaml
waste_collection_schedule:
    sources:
    - name: okc_gov
      args:
        objectID: OBJECT_ID
```

### Configuration Variables

**objectID**  
*(string) (required)*  
Object ID for your address from the public feed (`okc.schizo.dev`).

## Example

```yaml
waste_collection_schedule:
    sources:
    - name: okc_gov
      args:
        objectID: "1781151"
```

## How to find your Object ID

Using a browser, go to [data.okc.gov](https://data.okc.gov/portal/page/viewer?datasetName=Address%20Trash%20Services). Click on the `Map` tab, search for your address, then click on your house. Your schedule will be displayed.

Click on the `Table` tab, then click on the `Filter By Map` menu item, and click `Apply` to reduce the number of items being displayed. Note: the more you zoom in on your house in the previous step, the better this filter works.

Find your address in the filtered list and make a note of the `Object ID` number in the first column. This is the number you need to use as `objectID`.
