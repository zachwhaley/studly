package com.studly.network;

import com.octo.android.robospice.request.retrofit.RetrofitSpiceRequest;
import com.studly.model.StudlyMapping;

public class RequestStudlyGroups extends RetrofitSpiceRequest<StudlyMapping.List, StudlyApi> {

    private double mLatitude;
    private double mLongitude;
    
    public RequestStudlyGroups(double lat, double lon) {
        super(StudlyMapping.List.class, StudlyApi.class);
        mLatitude = lat;
        mLongitude = lon;
    }

    @Override
    public StudlyMapping.List loadDataFromNetwork() throws Exception {
        return getService().getMappings(mLatitude, mLongitude);
    }

}
