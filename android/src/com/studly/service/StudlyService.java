package com.studly.service;

import com.octo.android.robospice.retrofit.RetrofitGsonSpiceService;
import com.studly.network.StudlyApi;

public class StudlyService extends RetrofitGsonSpiceService {

    private static final String BASE_URL = "http://studly-manager.appspot.com";

    @Override
    protected String getServerUrl() {
        return BASE_URL;
    }

    @Override
    public void onCreate() {
        super.onCreate();
        addRetrofitInterface(StudlyApi.class);
    }
}
